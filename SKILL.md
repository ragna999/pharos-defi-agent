---
name: pharos-defi-agent
description: DeFi intelligence agent for the Pharos ecosystem. Check token safety, scan yields, analyze wallets, and batch-scan multiple tokens — powered by on-chain consensus data and multi-source analysis.
---

# Pharos DeFi Intelligence Agent

An AI agent that helps you navigate DeFi on Pharos safely. Check if tokens are safe, find the best yields, analyze wallet risk, and batch-scan multiple tokens — powered by on-chain consensus data from multi-agent reports AND real-time GoPlus Security API verification.

## Prerequisites

- Foundry installed (`cast` and `forge` available)
- `$PRIVATE_KEY` environment variable set (never hardcode)
- Pharos Atlantic Testnet RPC accessible

## Network Configuration

See `assets/networks.json` for RPC URLs, chain IDs, and explorer URLs.

## Capability Index

| User Intent | Capability | Reference File |
|---|---|---|
| "Is this token safe?" / "Check token 0x..." | Token Safety Check | `references/token-safety.md` |
| "What are the best yields?" / "Find yields on Pharos" | Yield Scanning | `references/yield-scan.md` |
| "Analyze wallet 0x..." / "Check this wallet" | Wallet Intelligence | `references/wallet-intel.md` |
| "Scan these tokens" / "Batch check" | Batch Scanning | `references/batch-scan.md` |
| "Verify with GoPlus" / "External security check" | GoPlus Security Scan | `references/goplus-scan.md` |
| "Report token safety" / "Submit safety report" | Write Safety Report | `references/token-safety.md` § Writing Reports |
| "Register yield protocol" / "Report yield data" | Write Yield Data | `references/yield-scan.md` § Writing Reports |

## On-Chain Contracts (Pharos Atlantic Testnet)

| Contract | Address | Purpose |
|---|---|---|
| TokenSafetyRegistry | `0xF11c856D021900f9c312e0e80913A7a0D6af40ED` | Multi-agent token safety consensus |
| YieldRegistry | See `assets/networks.json` | DeFi yield data registry |

## Example Interactions

### Token Safety
```
User: Is 0xF11c856D021900f9c312e0e80913A7a0D6af40ED safe?
Agent: [Queries getConsensus, returns safety report with verdict]
```

### Yield Scanning
```
User: What are the best yields on Pharos?
Agent: [Queries getAllProtocols, gets latest yield for each, returns ranked list]
```

### Wallet Analysis
```
User: Analyze wallet 0x8919fe5Aa2a18d69D1Ff869c2903B313F35e8061
Agent: [Gets balance, checks token holdings, cross-references with safety data]
```

### Batch Scanning
```
User: Check these tokens: 0xABC, 0xDEF, 0x123
Agent: [Calls batchIsTokenSafe, returns comparative table]
```

### Writing Data
```
User: Report safety for token 0xABC — score 85, no honeypot, 2% buy tax
Agent: [Confirms parameters, asks for gas confirmation, submits updateReport tx]
```

## General Error Handling

| Error | Cause | Fix |
|---|---|---|
| `contract not deployed` | Wrong network or address | Verify chain ID and contract address |
| `execution reverted` | Invalid parameters or contract state | Check input values, verify token address |
| `nonce too low` | Transaction already mined | Wait and retry |
| `insufficient funds` | Not enough PHAR for gas | Top up wallet with testnet PHAR |

## Security Reminders

- NEVER hardcode private keys — always use `$PRIVATE_KEY` env var
- ALWAYS verify token addresses before interacting
- Check consensus staleness before trusting safety scores
- Cross-reference on-chain data with external sources when possible

## Write Operation Pre-Check

Before ANY write operation (updateReport, reportYield, registerProtocol):

1. Verify the target address is valid (not zero address)
2. Verify you have sufficient PHAR for gas
3. Verify the operation parameters are within valid ranges
4. Confirm the intent with the user before executing

## Agent Guidelines

- When checking token safety, ALWAYS check consensus freshness first
- When scanning yields, filter by risk level based on user preference
- When analyzing wallets, cross-reference holdings with safety data
- Present results clearly: SAFE / CAUTION / AVOID with explanations
- If on-chain data is stale or missing, suggest running a fresh scan
