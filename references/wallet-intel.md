# Wallet Intelligence

## Overview

Analyze a wallet address on Pharos to understand its holdings, transaction patterns, and risk exposure. Cross-references token holdings with the TokenSafetyRegistry to identify risky assets in the portfolio.

## Network

- **RPC:** `https://atlantic.dplabs-internal.com`
- **Chain ID:** 688689 (Atlantic Testnet)
- **Explorer:** `https://atlantic.pharosscan.xyz`

## Query: Get Wallet Balance

**Intent:** "Check balance of 0xABC" / "How much PHAR does 0xABC have?"

**Using the bundled script:**
```bash
python3 scripts/rpc_helper.py wallet <WALLET_ADDRESS>
```

**Raw JSON-RPC:**
```bash
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["<WALLET_ADDRESS>","latest"],"id":1}'
```
**Returns:** Balance in wei (divide by 10^18 for PHAR)

## Query: Get ERC20 Token Balance

**Intent:** "Check token balance for 0xABC"

```bash
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"<TOKEN_ADDRESS>","data":"0x70a08231<WALLET_ADDRESS_PADDED>"},"latest"],"id":1}'
```
## Query: Get Transaction Count (Activity Level)

```bash
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionCount","params":["<WALLET_ADDRESS>","latest"],"id":1}'
```
**Returns:** Number of transactions sent from this address

## Query: Get Token Info

```bash
# Token name (0x06fdde03)
curl -s -X POST https://atlantic.dplabs-internal.com -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"<TOKEN_ADDRESS>","data":"0x06fdde03"},"latest"],"id":1}'

# Token symbol (0x95d89b41)
curl -s -X POST https://atlantic.dplabs-internal.com -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"<TOKEN_ADDRESS>","data":"0x95d89b41"},"latest"],"id":1}'

# Token decimals (0x313ce567)
curl -s -X POST https://atlantic.dplabs-internal.com -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"<TOKEN_ADDRESS>","data":"0x313ce567"},"latest"],"id":1}'

# Total supply (0x18160ddd)
curl -s -X POST https://atlantic.dplabs-internal.com -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"<TOKEN_ADDRESS>","data":"0x18160ddd"},"latest"],"id":1}'
```

## Cross-Reference with Safety Data

For each token in the wallet, check safety:

```bash
python3 scripts/rpc_helper.py safety <TOKEN_ADDRESS>

# Or raw:
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xF11c856D021900f9c312e0e80913A7a0D6af40ED","data":"0xe8f738e1<TOKEN_ADDRESS_PADDED>"},"latest"],"id":1}'
```
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
