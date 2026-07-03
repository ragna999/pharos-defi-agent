# Runtime Configuration

## Recommended Settings

| Setting | Value | Reasoning |
|---|---|---|
| Max concurrent sessions | 5 | Balance between throughput and resource usage. Safety/yield queries are fast (3-15s), so 5 concurrent sessions handles burst traffic well. |
| Max single execution time | 60 seconds | Most operations complete in 3-15 seconds. 60s allows for: network retries, batch scans of 10+ tokens, wallet analysis with many holdings. |
| Timeout for read operations | 30 seconds | Contract calls should complete within 10s normally. 30s allows for network congestion. |
| Timeout for write operations | 45 seconds | On-chain transactions need block confirmation. 45s covers typical Pharos block time + confirmation. |

## Execution Time Estimates by Task Type

| Task | Expected | Max (with retries) |
|---|---|---|
| Single token safety check | 3-8s | 15s |
| Yield scan (all protocols) | 8-15s | 30s |
| Wallet analysis (1-10 tokens) | 10-20s | 40s |
| Wallet analysis (10+ tokens) | 20-45s | 60s |
| Batch scan (5 tokens) | 8-15s | 25s |
| Batch scan (10+ tokens) | 15-30s | 45s |
| Write operation (report) | 10-20s | 45s |

## Resource Considerations

- Each session makes 1-5 RPC calls to Pharos testnet
- No external API dependencies (all on-chain)
- No heavy computation (just ABI encoding/decoding)
- Memory footprint is minimal
