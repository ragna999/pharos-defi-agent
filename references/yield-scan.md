# Yield Scanning

## Overview

Find and compare DeFi yield opportunities on the Pharos ecosystem. Query the on-chain YieldRegistry for registered protocols, their latest yield data, APY, TVL, and risk levels.

## Contract

- **Address:** See `assets/networks.json` → `yieldRegistry`
- **Network:** Pharos Atlantic Testnet (Chain ID: 688689)
- **RPC:** `https://atlantic.dplabs-internal.com`

## Query: Get All Protocols

**Intent:** "What yields are available?" / "List all protocols"

**Option A — Using the bundled script:**
```bash
python3 scripts/rpc_helper.py yields
```

**Option B — Raw JSON-RPC:**
```bash
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0x741c53eb"},"latest"],"id":1}'
```

## Query: Get Protocol Info

**Intent:** "Tell me about protocol 0xABC"

```bash
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0x21027dc5<PROTOCOL_ADDRESS_PADDED>"},"latest"],"id":1}'
```
**Categories:** `lending`, `dex`, `staking`, `yield`

## Query: Get Latest Yield

**Intent:** "What's the APY for protocol 0xABC?" / "Get yield for 0xABC"

```bash
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0xc2f8608d<PROTOCOL_ADDRESS_PADDED>"},"latest"],"id":1}'
```

**Note:** APY is in basis points (100 = 1%, 5000 = 50%)
**Note:** APY is in basis points (100 = 1%, 5000 = 50%)

## Query: Check Yield Freshness

```bash
cast call 0x6c65B773e1250D40e5902615FDd33d054C455ede   "isYieldFresh(address)(bool)"   <PROTOCOL_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

## Decision Logic

| Risk Level | Description | Recommendation |
|---|---|---|
| 1 (LOW) | Established protocol, audited, high TVL | Suitable for conservative users |
| 2 (MEDIUM) | Newer protocol or moderate TVL | Suitable for balanced risk/reward |
| 3 (HIGH) | New protocol, low TVL, unaudited | Only for degen plays |

## Response Format

```
Yield Opportunities on Pharos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Protocol: <name> (<category>)
  Pair:      <pair>
  APY:       <apy>% 
  TVL:       $<tvlUsd>
  Risk:      LOW/MEDIUM/HIGH
  Fresh:     Yes/No
  Verified:  Yes/No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sorted by: APY (highest first)
Filter:    <risk_level> risk only
```

## § Writing Reports

**Intent:** "Register a new protocol" / "Report yield data"

### Register Protocol

```bash
cast send 0x6c65B773e1250D40e5902615FDd33d054C455ede   "registerProtocol(address,string,string,address)"   <PROTOCOL_ADDRESS>   "<NAME>"   "<CATEGORY>"   <CONTRACT_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com   --private-key $PRIVATE_KEY
```

### Report Yield

```bash
cast send 0x6c65B773e1250D40e5902615FDd33d054C455ede   "reportYield(address,string,uint256,uint256,uint8)"   <PROTOCOL_ADDRESS>   "<PAIR>"   <APY_BASIS_POINTS>   <TVL_USD>   <RISK_LEVEL>   --rpc-url https://atlantic.dplabs-internal.com   --private-key $PRIVATE_KEY
```

**Parameters:**
| Param | Type | Range | Description |
|---|---|---|---|
| protocol | address | registered | Protocol address (must be registered) |
| pair | string | any | Trading pair (e.g., "PHAR/USDC") |
| apy | uint256 | 0+ | APY in basis points (5000 = 50%) |
| tvlUsd | uint256 | 0+ | Total value locked in USD |
| riskLevel | uint8 | 1-3 | 1=LOW, 2=MEDIUM, 3=HIGH |

## Error Messages from Contract

| Contract Error | Meaning | Agent Response |
|---|---|---|
| `Protocol not registered` | Address not in registry | "This protocol isn't registered yet. Would you like me to register it first?" |
| `Invalid risk level` | riskLevel not 1-3 | "Risk level must be 1 (LOW), 2 (MEDIUM), or 3 (HIGH)" |
| Empty protocol list | No protocols registered | "No yield protocols registered on Pharos yet." |
| Empty yield data | Protocol registered but no yields reported | "This protocol has no yield data yet. Would you like me to report current yields?" |

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `Protocol not registered` | Address not in registry | Register protocol first |
| `Invalid risk level` | riskLevel not 1-3 | Use 1, 2, or 3 |
| Empty protocol list | No protocols registered | Suggest registering protocols |
| ABI decode error with cast | Dynamic string returns | Use raw call: `cast call <addr> "function(address)" <param>` and decode manually |
