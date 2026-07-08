# Token Safety Data — Pharos Atlantic Testnet

**Source:** On-chain TokenSafetyRegistry (0xF11c856D021900f9c312e0e80913A7a0D6af40ED)
**Chain ID:** 688689
**Last updated:** Live from chain

## Pre-verified Tokens

### USDC (0xcfC8330f4BCAB529c625D12781b1C19466A9Fc8B)
- **Verdict:** SAFE ✅
- **Safety Score:** 100/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **Decimals:** 6

### WETH (0x7d211F77525ea39A0592794f793cC1036eEaccD5)
- **Verdict:** SAFE ✅
- **Safety Score:** 100/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **Decimals:** 18

### WBTC (0x0c64F03EEa5c30946D5c55B4b532D08ad74638a4)
- **Verdict:** SAFE ✅
- **Safety Score:** 90/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **Decimals:** 18

### USDT (0xE7E84B8B4f39C507499c40B4ac199B050e2882d5)
- **Verdict:** SAFE ✅
- **Safety Score:** 85/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **Decimals:** 6

### WPHRS (0x838800b758277CC111B2d48Ab01e5E164f8E9471)
- **Verdict:** UNKNOWN ❓
- **Safety Score:** 0/100
- **Honeypot:** No
- **Reports:** 0 agent(s)
- **Decimals:** 18
- **Note:** No safety data available. Not yet analyzed by agents.

---

## Decision Logic

| Condition | Verdict |
|---|---|
| Score >= 70 AND no honeypot AND taxes <= 10% | SAFE ✅ |
| Score 50-69 | CAUTION ⚠️ |
| Score < 50 OR honeypot | AVOID 🚫 |
| No reports (reportCount = 0) | UNKNOWN ❓ |

## How to Query Live Safety Data

For any token address, call the TokenSafetyRegistry via JSON-RPC:

```bash
# getConsensus(address) selector: 0xe8f738e1
# Pad the token address to 32 bytes (remove 0x, left-pad with zeros to 64 chars)

curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xF11c856D021900f9c312e0e80913A7a0D6af40ED","data":"0xe8f738e1<TOKEN_ADDRESS_PADDED>"},"latest"],"id":1}'
```

**Response decoding (each field is 32 bytes / 64 hex chars):**
- Bytes 0-31: avgScore (uint8, 0-100)
- Bytes 32-63: reportCount (uint8)
- Bytes 64-95: consensusHoneypot (bool)
- Bytes 96-127: avgBuyTax (uint8, 0-100)
- Bytes 128-159: avgSellTax (uint8, 0-100)
- Bytes 160-191: lastUpdated (uint256, unix timestamp)
- Bytes 192-223: isStale (bool)
