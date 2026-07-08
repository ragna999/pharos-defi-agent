# Token Safety Data — Pharos Atlantic Testnet

## Pre-verified Tokens

The following tokens have been verified via the TokenSafetyRegistry (0xF11c856D021900f9c312e0e80913A7a0D6af40ED) and GoPlus Security API.

### USDC (0xcfC8330f4BCAB529c625D12781b1C19466A9Fc8B)
- **Verdict:** SAFE ✅
- **Safety Score:** 100/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **GoPlus Verified:** Yes
- **Source:** On-chain consensus

### WETH (0x7d211F77525ea39A0592794f793cC1036eEaccD5)
- **Verdict:** SAFE ✅
- **Safety Score:** 100/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **GoPlus Verified:** Yes
- **Source:** On-chain consensus

### WBTC (0x0c64F03EEa5c30946D5c55B4b532D08ad74638a4)
- **Verdict:** SAFE ✅
- **Safety Score:** 90/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **GoPlus Verified:** Yes
- **Source:** On-chain consensus

### USDT (0xE7E84B8B4f39C507499c40B4ac199B050e2882d5)
- **Verdict:** SAFE ✅
- **Safety Score:** 85/100
- **Honeypot:** No
- **Buy Tax:** 0%
- **Sell Tax:** 0%
- **Reports:** 1 agent(s)
- **GoPlus Verified:** Yes
- **Source:** On-chain consensus

### WPHRS (0x838800b758277CC111B2d48Ab01e5E164f8E9471)
- **Verdict:** UNKNOWN ❓
- **Safety Score:** N/A
- **Reports:** 0 agent(s)
- **Source:** No on-chain data available

---

## How to Query Safety Data via JSON-RPC

For any token address, call the TokenSafetyRegistry:

```bash
# getConsensus(address) selector: 0xe8f738e1
# Pad the token address to 32 bytes (remove 0x, left-pad with zeros to 64 chars)

curl -s -X POST https://atlantic.dplabs-internal.com   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xF11c856D021900f9c312e0e80913A7a0D6af40ED","data":"0xe8f738e1<TOKEN_ADDRESS_PADDED>"},"latest"],"id":1}'
```

**Response decoding:**
- Bytes 0-31: avgScore (uint8, 0-100)
- Bytes 32-63: reportCount (uint8)
- Bytes 64-95: consensusHoneypot (bool)
- Bytes 96-127: avgBuyTax (uint8, 0-100)
- Bytes 128-159: avgSellTax (uint8, 0-100)
- Bytes 160-191: lastUpdated (uint256, unix timestamp)
- Bytes 192-223: isStale (bool)

**Decision logic:**
- Score >= 70, no honeypot, taxes <= 10% → SAFE ✅
- Score 50-69 → CAUTION ⚠️
- Score < 50 or honeypot → AVOID 🚫
- No reports → UNKNOWN ❓
