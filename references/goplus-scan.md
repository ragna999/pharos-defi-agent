# GoPlus Security Scan

## Overview

GoPlus Security provides real-time token safety data across multiple chains. Integrate GoPlus API calls as a complement to on-chain consensus data — use GoPlus when on-chain data is missing, stale, or needs verification.

## API Endpoint

**Base URL:** `https://api.gopluslabs.io/api/v1`

### Token Security Check

```
GET /token_security/{chain_id}?contract_addresses={address}
```

**Pharos Chain ID:** Check GoPlus docs for Pharos support. If Pharos not supported, use the general endpoint with the token address.

### Example: Check Token Safety

```bash
curl -s "https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=<TOKEN_ADDRESS>" | jq '.result["<TOKEN_ADDRESS>"]'
```

**Returns:**
```json
{
  "token_name": "Token Name",
  "token_symbol": "TKN",
  "owner_address": "0x...",
  "creator_address": "0x...",
  "total_supply": "1000000000",
  "holders_count": 1500,
  "is_open_source": 1,
  "is_proxy": 0,
  "is_mintable": 0,
  "can_take_back_ownership": 0,
  "owner_change_balance": 0,
  "hidden_owner": 0,
  "selfdestruct": 0,
  "external_call": 0,
  "is_honeypot": 0,
  "transfer_pausable": 0,
  "is_blacklisted": 0,
  "is_whitelisted": 0,
  "is_whitelisted": 0,
  "buy_tax": "0.02",
  "sell_tax": "0.03",
  "cannot_sell_all": 0,
  "slippage_modifiable": 0,
  "trading_cooldown": 0,
  "lp_total_supply": 500000,
  "lp_holder_count": 100,
  "lp_total_supply": 500000
}
```

## Key Fields to Extract

| GoPlus Field | Maps To | Description |
|---|---|---|
| `is_honeypot` | SafetyReport.isHoneypot | 1 = honeypot, 0 = safe |
| `is_mintable` | SafetyReport.isMintable | 1 = can mint new tokens |
| `buy_tax` | SafetyReport.buyTax | Buy tax percentage (0-100) |
| `sell_tax` | SafetyReport.sellTax | Sell tax percentage (0-100) |
| `holders_count` | SafetyReport.holderCount | Number of token holders |
| `is_open_source` | — | Contract source verified |
| `owner_change_balance` | — | Owner can change balances |
| `hidden_owner` | — | Contract has hidden owner |
| `selfdestruct` | — | Contract can self-destruct |
| `cannot_sell_all` | — | Holders can't sell all tokens |
| `lp_total_supply` | — | Liquidity pool size |
| `lp_holder_count` | — | Number of LP holders |

## Decision Logic: GoPlus → Safety Score

Convert GoPlus data to a 0-100 safety score:

| Factor | Weight | Scoring |
|---|---|---|
| Honeypot | -30 | is_honeypot=1 → -30 points |
| Mintable | -10 | is_mintable=1 → -10 points |
| Hidden owner | -15 | hidden_owner=1 → -15 points |
| Self-destruct | -10 | selfdestruct=1 → -10 points |
| Buy tax | -0 to -15 | buy_tax * 1.5 (cap at 15) |
| Sell tax | -0 to -15 | sell_tax * 1.5 (cap at 15) |
| Can't sell all | -10 | cannot_sell_all=1 → -10 points |
| Open source | +5 | is_open_source=1 → +5 points |
| Low LP | -5 | lp_total_supply < 10000 → -5 points |

**Base score:** 100
**Final score:** base - penalties

## Integration Flow

When user asks "Is token 0xABC safe?":

```
1. Check on-chain consensus FIRST
   └─ cast call TokenSafetyRegistry.getConsensus(token)

2. If consensus exists AND is fresh (<24h):
   └─ Return on-chain consensus data
   
3. If NO consensus OR stale:
   └─ Fetch from GoPlus API
   └─ Convert to SafetyReport format
   └─ Calculate safety score
   └─ Submit to TokenSafetyRegistry (write operation)
   └─ Return the freshly computed data

4. This way, the NEXT user asking about the same token
   gets instant on-chain consensus (agent improved the system!)
```

## Response Format

```
Token Safety Analysis: <TOKEN_ADDRESS>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: On-chain consensus + GoPlus verification

Verdict:     SAFE ✅ / CAUTION ⚠️ / AVOID 🚫
Score:       <score>/100

Security Checks:
  Honeypot:        No ✅
  Mintable:        No ✅
  Hidden Owner:    No ✅
  Self-destruct:   No ✅
  Open Source:     Yes ✅
  Buy Tax:         2%
  Sell Tax:        3%
  Can Sell All:    Yes ✅
  Holders:         1,500
  LP Holders:      100
  LP Supply:       $500,000

Data Sources:
  On-chain:        <reportCount> agent reports
  GoPlus:          ✅ Verified
  Last Updated:    <timestamp>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| GoPlus API timeout | Network issue | Retry once, fall back to on-chain data only |
| Token not found on GoPlus | Pharos token not indexed | Use on-chain data only, note "GoPlus: not available" |
| Rate limited | Too many API calls | Cache results, reduce call frequency |
| Invalid response | API format changed | Log error, return on-chain data only |

## Agent Guidelines

- ALWAYS check on-chain consensus first (faster, no API cost)
- Use GoPlus as SECONDARY verification or when on-chain data is missing
- When writing GoPlus data on-chain, note the source in the report
- If both sources agree → high confidence verdict
- If sources disagree → present both, flag the discrepancy
- GoPlus may not support Pharos chain — handle gracefully
