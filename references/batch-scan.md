# Batch Scanning

## Overview

Scan multiple tokens at once for safety using the TokenSafetyRegistry's batch function. Efficient for comparing tokens or checking a portfolio's risk exposure.

## Contract

- **Address:** `0xF11c856D021900f9c312e0e80913A7a0D6af40ED`
- **Network:** Pharos Atlantic Testnet (Chain ID: 688689)
- **RPC:** `https://atlantic.dplabs-internal.com`

## Query: Batch Safety Check

**Intent:** "Scan these tokens" / "Check multiple tokens at once" / "Which of these are safe?"

**Using the bundled script:**
```bash
python3 scripts/rpc_helper.py batch <TOKEN_1>,<TOKEN_2>,<TOKEN_3>
```

**Raw JSON-RPC:**
```bash
# For each token, call getConsensus individually:
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xF11c856D021900f9c312e0e80913A7a0D6af40ED","data":"0xe8f738e1<TOKEN_ADDRESS_PADDED>"},"latest"],"id":1}'
```

**Note:** The `batchIsTokenSafe` function (selector `0xbadb7021`) requires ABI encoding of an address array. Use the bundled script for convenience.
## Query: Get Detailed Reports for Multiple Tokens

For each token in the batch, get full consensus:

```bash
# For each token:
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xF11c856D021900f9c312e0e80913A7a0D6af40ED","data":"0xe8f738e1<TOKEN_ADDRESS_PADDED>"},"latest"],"id":1}'
```
**Intent:** "Show all reports for token 0xABC"

```bash
cast call 0xF11c856D021900f9c312e0e80913A7a0D6af40ED   "getMultiReporterReports(address)((uint8,bool,bool,uint8,uint8,uint256,uint256,address)[])"   <TOKEN_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

**Returns:** Array of SafetyReport structs from all reporters

## Response Format

```
Batch Safety Scan Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tokens scanned: <count>

┌─────┬──────────────────────────────────────┬──────────┬─────────┬────────┐
│  #  │ Token Address                        │ Verdict  │ Score   │ Honeypot│
├─────┼──────────────────────────────────────┼──────────┼─────────┼────────┤
│  1  │ 0xABC...def                          │ ✅ SAFE  │ 85/100  │ No     │
│  2  │ 0x123...456                          │ 🚫 AVOID │ 20/100  │ Yes!   │
│  3  │ 0x789...abc                          │ ❓ UNKNOWN│ N/A     │ N/A    │
│  4  │ 0xDEF...012                          │ ⚠️ CAUTION│ 55/100  │ No     │
└─────┴──────────────────────────────────────┴──────────┴─────────┴────────┘

Summary:
  Safe:    <count> ✅
  Caution: <count> ⚠️
  Avoid:   <count> 🚫
  Unknown: <count> ❓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Agent Guidelines

- Parse user input to extract multiple token addresses
- If user provides a comma-separated list, split and validate each
- If user provides a wallet address, first get token holdings then batch scan
- Present results in a table format for easy comparison
- Highlight any AVOID/honeypot tokens prominently
- For UNKNOWN tokens, offer to run a fresh safety analysis
