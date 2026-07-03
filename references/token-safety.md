# Token Safety Check

## Overview

Check if a token on Pharos is safe to interact with by querying the on-chain TokenSafetyRegistry consensus data. The registry aggregates safety reports from multiple independent agents to produce a consensus score.

## Contract

- **Address:** `0xF11c856D021900f9c312e0e80913A7a0D6af40ED`
- **Network:** Pharos Atlantic Testnet (Chain ID: 688689)
- **RPC:** `https://atlantic.dplabs-internal.com`

## Query: Check Token Safety

**Intent:** "Is token 0xABC safe?" / "Check safety of 0xABC"

### Step 1: Get Consensus Report

```bash
cast call 0xF11c856D021900f9c312e0e80913A7a0D6af40ED   "getConsensus(address)(uint8,uint8,bool,uint8,uint8,uint256,bool)"   <TOKEN_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

**Returns:** `(avgScore, reportCount, consensusHoneypot, avgBuyTax, avgSellTax, lastUpdated, isStale)`

### Step 2: Quick Safety Boolean

```bash
cast call 0xF11c856D021900f9c312e0e80913A7a0D6af40ED   "isTokenSafe(address)(bool)"   <TOKEN_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

**Returns:** `true` if safe, `false` if unsafe or no data

### Step 3: Check Staleness

```bash
cast call 0xF11c856D021900f9c312e0e80913A7a0D6af40ED   "isConsensusStale(address)(bool)"   <TOKEN_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

## Decision Logic

| Condition | Verdict |
|---|---|
| `avgScore >= 70` AND NOT `consensusHoneypot` AND `avgBuyTax <= 10` AND `avgSellTax <= 10` | **SAFE** ✅ |
| `avgScore >= 50` AND `avgScore < 70` | **CAUTION** ⚠️ |
| `avgScore < 50` OR `consensusHoneypot` | **AVOID** 🚫 |
| `reportCount == 0` | **UNKNOWN** ❓ — no consensus data available |
| `isStale == true` | **STALE** ⏰ — data older than 24h, suggest re-scan |

## Response Format

```
Token Safety Report: <TOKEN_ADDRESS>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verdict:     SAFE ✅ / CAUTION ⚠️ / AVOID 🚫 / UNKNOWN ❓
Score:       <avgScore>/100
Honeypot:    Yes/No
Buy Tax:     <avgBuyTax>%
Sell Tax:    <avgSellTax>%
Reports:     <reportCount> agent(s)
Last Update: <timestamp> (<freshness>)
Consensus:   <explanation>
```

## § Writing Reports

**Intent:** "Report token safety for 0xABC"

### Submit Safety Report

```bash
cast send 0xF11c856D021900f9c312e0e80913A7a0D6af40ED   "updateReport(address,uint8,bool,bool,uint8,uint8,uint256)"   <TOKEN_ADDRESS>   <SCORE>   <IS_HONEYPOT>   <IS_MINTABLE>   <BUY_TAX>   <SELL_TAX>   <HOLDER_COUNT>   --rpc-url https://atlantic.dplabs-internal.com   --private-key $PRIVATE_KEY
```

**Parameters:**
| Param | Type | Range | Description |
|---|---|---|---|
| token | address | valid address | Token contract address |
| score | uint8 | 0-100 | Safety score (70+ = safe) |
| isHoneypot | bool | true/false | Can holders sell? |
| isMintable | bool | true/false | Can supply increase? |
| buyTax | uint8 | 0-100 | Buy tax percentage |
| sellTax | uint8 | 0-100 | Sell tax percentage |
| holderCount | uint256 | 0+ | Number of token holders |

## Error Messages from Contract

The contract returns these specific error messages. Use them to give users clear feedback:

| Contract Error | Meaning | Agent Response |
|---|---|---|
| `Invalid token address` | Zero address passed | "Please provide a valid token address (not 0x000...000)" |
| `Invalid tax` | buyTax or sellTax > 100 | "Tax values must be between 0 and 100" |
| No reverts, empty data | Token has no reports | "No safety data found for this token. Would you like me to submit a report?" |

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `contract not deployed` | Wrong network or address | Verify chain ID (688689) and contract address |
| `execution reverted` | Invalid parameters or contract state | Check input values, verify token address |
| `nonce too low` | Transaction already mined | Wait and retry |
| `insufficient funds` | Not enough PHAR for gas | Top up wallet with testnet PHAR |
| Empty consensus data (all zeros) | No reports exist for this token | Suggest submitting a safety report first |
| `isTokenSafe` returns false with no data | Default state — no reports | "This token hasn't been analyzed yet. No safety data available." |

| Error | Cause | Fix |
|---|---|---|
| `Invalid token address` | Zero address passed | Verify token address |
| `Invalid tax` | Tax > 100 | Check buyTax/sellTax values |
| No consensus data | No reports exist | Suggest submitting a report first |
