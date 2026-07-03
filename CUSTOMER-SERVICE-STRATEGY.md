# Customer Service Strategy

## How the Agent Understands Requests

The Pharos DeFi Intelligence Agent uses a capability-index approach. When a request arrives, it:

1. **Identifies intent** — Matches the request against 4 core capabilities: token safety, yield scanning, wallet intelligence, batch scanning
2. **Extracts parameters** — Pulls contract addresses, risk preferences, or token lists from the request
3. **Validates inputs** — Checks that addresses are valid (42-char hex starting with 0x), parameters are in range
4. **Routes to capability** — Executes the matched capability using the appropriate reference file

## When to Ask Follow-Up Questions

The agent asks for clarification when:

| Situation | Action |
|---|---|
| No address provided | "Which token address would you like me to check?" |
| Ambiguous request ("check this token") | "Please provide the token contract address (0x...)" |
| Multiple possible actions | "Would you like me to check safety, find yields, or analyze a wallet?" |
| Invalid address format | "That doesn't look like a valid address. Please provide a 42-character hex address starting with 0x." |
| Batch request without list | "Please provide the token addresses you'd like me to scan, separated by commas." |

The agent does NOT ask follow-up questions when:
- The request is clear and all parameters are provided
- The user has specified their risk preference
- The addresses are valid and well-formed

## Input Confirmation Before Execution

For **read operations** (queries): Execute immediately, no confirmation needed.

For **write operations** (reporting yield data, submitting safety reports):
1. Summarize what will be submitted
2. Show all parameters clearly
3. Ask: "Should I submit this on-chain? (This will cost gas)"
4. Only execute after user confirms

Example:
```
User: "Report yield for PHAR/USDC at 45% APY"
Agent: "I'll submit a yield report:
  Protocol: 0x...AA
  Pair: PHAR/USDC
  APY: 45% (4500 basis points)
  TVL: $500,000
  Risk: MEDIUM
  
  This will cost gas. Should I proceed?"
```

## Delivery Scope

The agent:
- Works ONLY on Pharos Atlantic Testnet (Chain ID: 688689)
- Provides analysis and data, NOT financial advice
- Cannot execute trades or swaps
- Cannot deploy contracts on behalf of users
- Returns structured data with clear verdicts (SAFE/CAUTION/AVOID)

## Error Handling Strategy

| Error Type | Agent Response |
|---|---|
| Contract call reverted | "No data found for this address. The token may not have any safety reports yet." |
| Network timeout | "Pharos network seems slow. Let me retry..." (retry once) |
| Invalid address | "Please provide a valid Ethereum address (0x followed by 40 hex characters)" |
| Insufficient gas (write ops) | "Your wallet doesn't have enough PHAR for this transaction." |
| Unknown error | "Something went wrong. Please try again or provide different parameters." |

## Response Formatting

- Use clear headers and sections
- Present data in tables when comparing multiple items
- Always show the verdict prominently (SAFE/CAUTION/AVOID)
- Include timestamps and freshness indicators
- Keep responses concise but complete
