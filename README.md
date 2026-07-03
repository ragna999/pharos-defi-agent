# Pharos DeFi Intelligence Agent

> AI-powered DeFi safety and yield analysis for the Pharos ecosystem — built for Agent Carnival Phase 2.

## What It Does

A Service Agent on AnvitaFlow that provides:

- **Token Safety Checks** — Multi-agent on-chain consensus via TokenSafetyRegistry (score 0-100, honeypot detection, tax analysis)
- **Yield Discovery** — Find and compare DeFi yields across Pharos protocols (APY, TVL, risk levels)
- **Wallet Intelligence** — Analyze wallet holdings and cross-reference with safety data (portfolio risk assessment)
- **Batch Scanning** — Scan multiple tokens at once for portfolio risk assessment

## How It Works

```
User → Anvita On Chat → Steward Agent → Marketplace
  → Finds Pharos DeFi Intelligence Agent
  → Executes capability (safety/yield/wallet/batch)
  → Returns structured analysis
```

## Architecture

```
pharos-defi-agent/
├── SKILL.md                    ← Entry point + capability index
├── references/
│   ├── token-safety.md         ← Token safety check procedures
│   ├── yield-scan.md           ← Yield scanning procedures
│   ├── wallet-intel.md         ← Wallet analysis procedures
│   └── batch-scan.md           ← Batch scanning procedures
├── assets/
│   ├── networks.json           ← Pharos network config
│   ├── tokens.json             ← Known token addresses
│   └── abi/
│       ├── TokenSafetyRegistry.json
│       └── YieldRegistry.json
├── AGENT-CARD.md               ← Marketplace listing draft
├── CUSTOMER-SERVICE-STRATEGY.md ← Agent behavior & error handling
└── RUNTIME-CONFIG.md           ← Execution limits & timing
```

## On-Chain Contracts (Pharos Atlantic Testnet — Chain ID: 688689)

| Contract | Address | Version |
|---|---|---|
| TokenSafetyRegistry | `0xF11c856D021900f9c312e0e80913A7a0D6af40ED` | v0.2.0 (multi-agent consensus) |
| YieldRegistry | `0x6c65B773e1250D40e5902615FDd33d054C455ede` | v0.2.0 (yield reporting) |

**RPC:** `https://atlantic.dplabs-internal.com`
**Explorer:** `https://atlantic.pharosscan.xyz`

## Contract Capabilities

### TokenSafetyRegistry
| Function | Type | Description |
|---|---|---|
| `updateReport()` | Write | Submit safety report (score, honeypot, mintable, taxes, holders) |
| `getConsensus()` | Read | Get multi-agent consensus (avgScore, reportCount, honeypot, taxes) |
| `isTokenSafe()` | Read | Quick boolean safety check |
| `batchIsTokenSafe()` | Read | Check multiple tokens at once |
| `getReporterCount()` | Read | Number of reports for a token |
| `isConsensusStale()` | Read | Check if data is >24h old |

### YieldRegistry
| Function | Type | Description |
|---|---|---|
| `registerProtocol()` | Write | Register a new DeFi protocol |
| `reportYield()` | Write | Submit yield data (pair, APY, TVL, risk) |
| `getLatestYield()` | Read | Get latest yield for a protocol |
| `getAllProtocols()` | Read | List all registered protocols |
| `getProtocol()` | Read | Get protocol info (name, category, verified) |
| `isYieldFresh()` | Read | Check if yield data is <24h old |

## Phase 1 Foundation

This agent builds on our Phase 1 winning submission:
- TokenSafetyRegistry contract (multi-agent consensus)
- YieldRegistry contract (DeFi yield data)
- 36 passing tests
- Pharos Skill Engine format

## Submission

- **Platform:** AnvitaFlow Developer Console (https://flow.anvita.xyz/service-agents)
- **Upload opens:** July 8, 2026 — 7:00 PM HKT
- **Deadline:** July 10, 2026 — 6:00 PM HKT
- **Requirements:** GitHub repo, video tutorial, skill package (.zip)

## License

MIT
