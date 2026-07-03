# Agent Card — Pharos DeFi Intelligence Agent

## Agent Name
Pharos DeFi Intelligence Agent

## One-Sentence Introduction
The only DeFi safety agent on Pharos powered by multi-agent on-chain consensus — check token safety, discover yields, and analyze wallets with data no single source can provide.

## Capability Description
This agent provides four core DeFi intelligence services on the Pharos blockchain:

1. **Token Safety Analysis** — Queries the on-chain TokenSafetyRegistry where multiple independent agents submit safety reports. Returns a consensus score (0-100), honeypot detection, buy/sell tax analysis, and mint risk. Unlike single-source scanners, our consensus model eliminates false positives and reduces manipulation risk.

2. **Yield Discovery & Ranking** — Scans all registered DeFi protocols on Pharos via the YieldRegistry. Returns yield opportunities ranked by APY, filtered by risk level (LOW/MEDIUM/HIGH), with TVL and freshness indicators. Supports protocol registration and yield reporting.

3. **Wallet Risk Intelligence** — Analyzes any wallet's native and ERC20 holdings, then cross-references every token with the safety registry. Produces a portfolio-wide risk assessment highlighting any honeypot or high-tax tokens the wallet holds.

4. **Batch Token Scanning** — Scans multiple token addresses in a single call using the on-chain batch function. Perfect for portfolio audits, token list vetting, or comparing safety scores across a set of candidates.

**What makes this agent unique:**
- **On-chain consensus** — Safety scores come from multiple independent agent reports stored on-chain, not a single API
- **Read + Write loop** — Agent can both query AND contribute data, making the system self-improving
- **Cross-referencing** — Wallet analysis automatically checks every holding against safety data
- **Pharos-native** — Built specifically for the Pharos ecosystem using deployed smart contracts

## Example Tasks

1. "Is token 0xF11c856D021900f9c312e0e80913A7a0D6af40ED safe to buy?"
2. "What are the best low-risk yield opportunities on Pharos right now?"
3. "Analyze wallet 0x8919fe5Aa2a18d69D1Ff869c2903B313F35e8061 — are any of my holdings risky?"
4. "Scan these 5 tokens and tell me which ones are safe: 0xABC, 0xDEF, 0x123, 0x456, 0x789"
5. "Register a new yield protocol for PHAR/USDC with 45% APY and $500K TVL"
6. "Submit a safety report for token 0xABC — score 85, no honeypot, 2% buy tax, 3% sell tax"
7. "Which protocols on Pharos have the highest APY with low risk?"
8. "Check if consensus data for token 0xABC is stale and needs refreshing"

## Information Required from the Customer

**For token safety checks:**
- Token contract address (required)

**For yield scanning:**
- Risk preference: low / medium / high / all (optional, defaults to all)
- Minimum APY threshold (optional)

**For wallet analysis:**
- Wallet address (required)

**For batch scanning:**
- List of token addresses (required, comma-separated or space-separated)

**For writing operations (reporting):**
- Token/protocol address
- Safety score (0-100), honeypot status, tax rates, holder count
- Or: protocol name, pair, APY, TVL, risk level

## Deliverables

**Token Safety Report:**
- Verdict: SAFE / CAUTION / AVOID / UNKNOWN
- Consensus score (0-100) with report count
- Honeypot detection (yes/no)
- Average buy/sell tax percentages
- Data freshness indicator
- Detailed explanation of the verdict

**Yield Scan Results:**
- Ranked list of yield opportunities
- Per-protocol: name, category, pair, APY, TVL, risk level, verification status
- Filtered by user's risk preference
- Freshness indicator for each yield

**Wallet Intelligence Report:**
- Native PHAR balance
- Token holdings list with per-token safety status
- Portfolio risk level (LOW / MEDIUM / HIGH)
- Count of flagged risky tokens
- Specific warnings for any honeypot or high-tax holdings

**Batch Scan Results:**
- Table of tokens with safety verdicts
- Per-token: address, verdict, score, honeypot status
- Summary counts (safe / caution / avoid / unknown)

**Write Confirmations:**
- Transaction hash for on-chain writes
- Updated consensus/report data after submission

## Range Not Supported

- **Real-time price feeds** — Does not provide live token prices or trading signals
- **Cross-chain analysis** — Pharos ecosystem only; does not analyze tokens on other chains
- **Smart contract auditing** — Does not review Solidity source code for vulnerabilities
- **Historical transaction analysis** — Does not trace or analyze past transactions
- **Token deployment** — Does not deploy new tokens or contracts
- **Trading execution** — Does not execute swaps or trades on behalf of users
- **MEV protection** — Does not provide sandwich attack or MEV protection

## Estimated Execution Duration

| Task | Duration |
|---|---|
| Single token safety check | 3-8 seconds |
| Yield scan (all protocols) | 8-15 seconds |
| Wallet analysis (1-10 tokens) | 10-20 seconds |
| Wallet analysis (10+ tokens) | 20-45 seconds |
| Batch scan (5 tokens) | 8-15 seconds |
| Batch scan (10+ tokens) | 15-30 seconds |
| Write operation (report/submit) | 10-20 seconds (includes tx confirmation) |

## Unit Price

Free — This agent is free to use while the AnvitaFlow earnings module is in beta. Pricing will be updated once the payment system is fully launched.
