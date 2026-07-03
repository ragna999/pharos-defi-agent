# Wallet Intelligence

## Overview

Analyze a wallet address on Pharos to understand its holdings, transaction patterns, and risk exposure. Cross-references token holdings with the TokenSafetyRegistry to identify risky assets in the portfolio.

## Network

- **RPC:** `https://atlantic.dplabs-internal.com`
- **Chain ID:** 688689 (Atlantic Testnet)
- **Explorer:** `https://atlantic.pharosscan.xyz`

## Query: Get Wallet Balance

**Intent:** "Check balance of 0xABC" / "How much PHAR does 0xABC have?"

```bash
cast balance <WALLET_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

**Returns:** Balance in wei (divide by 10^18 for PHAR)

## Query: Get ERC20 Token Balance

**Intent:** "Check token balance for 0xABC"

```bash
cast call <TOKEN_ADDRESS>   "balanceOf(address)(uint256)"   <WALLET_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

**Returns:** Token balance (divide by 10^decimals for human-readable)

## Query: Get Transaction Count (Activity Level)

```bash
cast tx-count <WALLET_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

**Returns:** Number of transactions sent from this address

## Query: Get Token Info

```bash
# Token name
cast call <TOKEN_ADDRESS> "name()(string)" --rpc-url https://atlantic.dplabs-internal.com

# Token symbol
cast call <TOKEN_ADDRESS> "symbol()(string)" --rpc-url https://atlantic.dplabs-internal.com

# Token decimals
cast call <TOKEN_ADDRESS> "decimals()(uint8)" --rpc-url https://atlantic.dplabs-internal.com

# Total supply
cast call <TOKEN_ADDRESS> "totalSupply()(uint256)" --rpc-url https://atlantic.dplabs-internal.com
```

## Cross-Reference with Safety Data

For each token in the wallet, check safety:

```bash
cast call 0xF11c856D021900f9c312e0e80913A7a0D6af40ED   "getConsensus(address)(uint8,uint8,bool,uint8,uint8,uint256,bool)"   <TOKEN_ADDRESS>   --rpc-url https://atlantic.dplabs-internal.com
```

## Response Format

```
Wallet Intelligence Report: <WALLET_ADDRESS>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Native Balance:  <balance> PHAR
Transactions:    <tx_count>
Activity Level:  HIGH / MEDIUM / LOW / DORMANT

Token Holdings:
┌─────────────┬─────────────┬────────┬─────────────┐
│ Token       │ Balance     │ Safety │ Risk        │
├─────────────┼─────────────┼────────┼─────────────┤
│ PHAR        │ 1,000.00    │ ✅ N/A │ Native      │
│ TOKEN_A     │ 500.00      │ ✅ SAFE│ Score: 85   │
│ TOKEN_B     │ 1,000.00    │ 🚫 AVOID│ Honeypot! │
└─────────────┴─────────────┴────────┴─────────────┘

Portfolio Risk:  LOW / MEDIUM / HIGH
Risky Tokens:    <count> flagged
Recommendation:  <summary>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Decision Logic

| Activity Level | Transaction Count |
|---|---|
| HIGH | > 100 transactions |
| MEDIUM | 10-100 transactions |
| LOW | 1-10 transactions |
| DORMANT | 0 transactions |

| Portfolio Risk | Condition |
|---|---|
| LOW | All holdings SAFE, no honeypots |
| MEDIUM | Some CAUTION tokens or unknown tokens |
| HIGH | Any AVOID/honeypot tokens in portfolio |

## Agent Guidelines

- Always check native PHAR balance first
- For known tokens on Pharos, check `assets/tokens.json` for addresses
- Cross-reference every token with TokenSafetyRegistry
- Flag any honeypot or high-tax tokens immediately
- If a token has no safety data, mark as UNKNOWN and suggest running a safety check
