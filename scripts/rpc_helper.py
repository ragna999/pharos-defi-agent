#!/usr/bin/env python3
"""Pharos DeFi Intelligence RPC Helper

Usage:
    python3 rpc_helper.py safety <token_address>
    python3 rpc_helper.py yields
    python3 rpc_helper.py wallet <wallet_address>
    python3 rpc_helper.py batch <token1,token2,...>
    python3 rpc_helper.py goplus <token_address> [chain_id]

All calls go through standard JSON-RPC eth_call -- no Foundry needed.
"""

import json
import sys
import urllib.request
import urllib.error

RPC_URL = "https://atlantic.dplabs-internal.com"
CHAIN_ID = 688689

TOKEN_SAFETY = "0xF11c856D021900f9c312e0e80913A7a0D6af40ED"
YIELD_REGISTRY = "0x6c65B773e1250D40e5902615FDd33d054C455ede"

# Function selectors (keccak256 first 4 bytes)
SELECTORS = {
    "getConsensus": "0xe8f738e1",
    "isTokenSafe": "0x54cad8a6",
    "batchIsTokenSafe": "0xbadb7021",
    "getAllProtocols": "0x741c53eb",
    "getProtocol": "0x21027dc5",
    "getLatestYield": "0xc2f8608d",
    "isYieldFresh": "0xc4a5e22f",
    "balanceOf": "0x70a08231",
    "getReporterCount": "0x0b8fe34b",
    "isConsensusStale": "0x62d36c66",
}


def pad_address(addr):
    return addr.lower().replace("0x", "").zfill(64)


def eth_call(to, data):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": to, "data": data}, "latest"],
        "id": 1
    }).encode()
    req = urllib.request.Request(RPC_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if "error" in result:
                return {"error": result["error"]["message"]}
            return result.get("result", "0x")
    except Exception as e:
        return {"error": str(e)}


def get_consensus(token_addr):
    data = SELECTORS["getConsensus"] + pad_address(token_addr)
    result = eth_call(TOKEN_SAFETY, data)
    if isinstance(result, dict) and "error" in result:
        return result
    d = result[2:]
    if len(d) < 448:
        return {"error": "Empty consensus data"}
    avg_score = int(d[0:64], 16)
    report_count = int(d[64:128], 16)
    honeypot = int(d[128:192], 16) == 1
    buy_tax = int(d[192:256], 16)
    sell_tax = int(d[256:320], 16)
    last_updated = int(d[320:384], 16)
    is_stale = int(d[384:448], 16) == 1
    if report_count == 0:
        verdict = "UNKNOWN"
    elif avg_score < 50 or honeypot:
        verdict = "AVOID"
    elif avg_score < 70:
        verdict = "CAUTION"
    else:
        verdict = "SAFE"
    return {
        "verdict": verdict,
        "score": avg_score,
        "reports": report_count,
        "honeypot": honeypot,
        "buy_tax": buy_tax,
        "sell_tax": sell_tax,
        "last_updated": last_updated,
        "stale": is_stale,
    }


def is_token_safe(token_addr):
    data = SELECTORS["isTokenSafe"] + pad_address(token_addr)
    result = eth_call(TOKEN_SAFETY, data)
    if isinstance(result, dict) and "error" in result:
        return result
    return {"safe": int(result, 16) == 1}


def get_all_protocols():
    data = SELECTORS["getAllProtocols"]
    result = eth_call(YIELD_REGISTRY, data)
    if isinstance(result, dict) and "error" in result:
        return result
    if result == "0x" or len(result) < 66:
        return []
    d = result[2:]
    length = int(d[64:128], 16)
    addresses = []
    for i in range(length):
        start = 128 + (i * 64)
        addr = "0x" + d[start:start+64][-40:]
        addresses.append(addr)
    return addresses


def get_latest_yield(protocol_addr):
    data = SELECTORS["getLatestYield"] + pad_address(protocol_addr)
    result = eth_call(YIELD_REGISTRY, data)
    if isinstance(result, dict) and "error" in result:
        return result
    d = result[2:]
    if len(d) < 448:
        return {"error": "No yield data"}
    protocol = "0x" + d[0:64][-40:]
    pair_offset = int(d[64:128], 16) * 2
    pair_length = int(d[pair_offset:pair_offset+64], 16)
    pair_hex = d[pair_offset+64:pair_offset+64+pair_length*2]
    pair = bytes.fromhex(pair_hex).decode("utf-8") if pair_length > 0 else "N/A"
    apy = int(d[128:192], 16)
    tvl = int(d[192:256], 16)
    risk = int(d[256:320], 16)
    reported_at = int(d[320:384], 16)
    reporter = "0x" + d[384:448][-40:]
    risk_label = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}.get(risk, "UNKNOWN")
    return {
        "protocol": protocol,
        "pair": pair,
        "apy_pct": apy / 100,
        "tvl_usd": tvl,
        "risk": risk_label,
        "reported_at": reported_at,
        "reporter": reporter,
    }


def get_balance(wallet_addr):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [wallet_addr, "latest"],
        "id": 1
    }).encode()
    req = urllib.request.Request(RPC_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if "error" in result:
                return {"error": result["error"]["message"]}
            balance_wei = int(result.get("result", "0x0"), 16)
            return {"balance_wei": balance_wei, "balance_phar": balance_wei / 1e18}
    except Exception as e:
        return {"error": str(e)}


def batch_safety(token_addrs):
    results = []
    for addr in token_addrs:
        consensus = get_consensus(addr.strip())
        results.append({"address": addr.strip(), **consensus})
    return results


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]

    if cmd == "safety" and len(sys.argv) >= 3:
        token = sys.argv[2]
        consensus = get_consensus(token)
        safe = is_token_safe(token)
        print(json.dumps({"consensus": consensus, "is_safe": safe}, indent=2))

    elif cmd == "yields":
        protocols = get_all_protocols()
        if isinstance(protocols, dict) and "error" in protocols:
            print(json.dumps(protocols, indent=2))
            return
        yields = []
        for p in protocols:
            y = get_latest_yield(p)
            yields.append(y)
        yields.sort(key=lambda x: x.get("apy_pct", 0), reverse=True)
        print(json.dumps({"protocols": len(protocols), "yields": yields}, indent=2))

    elif cmd == "wallet" and len(sys.argv) >= 3:
        wallet = sys.argv[2]
        balance = get_balance(wallet)
        print(json.dumps({"wallet": wallet, "balance": balance}, indent=2))

    elif cmd == "batch" and len(sys.argv) >= 3:
        tokens = sys.argv[2].split(",")
        results = batch_safety(tokens)
        print(json.dumps({"scanned": len(results), "results": results}, indent=2))

    elif cmd == "goplus" and len(sys.argv) >= 3:
        token = sys.argv[2]
        chain = sys.argv[3] if len(sys.argv) >= 4 else "1"
        url = f"https://api.gopluslabs.io/api/v1/token_security/{chain}?contract_addresses={token}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                print(json.dumps(data, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}, indent=2))

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
