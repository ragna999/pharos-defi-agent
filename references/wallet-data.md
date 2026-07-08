# Wallet Intelligence Data

## How to Analyze a Wallet

### Step 1: Get Native Balance

```bash
curl -s -X POST https://atlantic.dplabs-internal.com   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["<WALLET_ADDRESS>","latest"],"id":1}'
```

Result is in wei. Divide by 10^18 for PHAR.

### Step 2: Get Transaction Count

```bash
curl -s -X POST https://atlantic.dplabs-internal.com   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"eth_getTransactionCount","params":["<WALLET_ADDRESS>","latest"],"id":1}'
```

Activity levels:
- > 100 txns → HIGH
- 10-100 txns → MEDIUM
- 1-10 txns → LOW
- 0 txns → DORMANT

### Step 3: Get ERC20 Balances

For each known token, check balance:

```bash
# balanceOf(address) selector: 0x70a08231
curl -s -X POST https://atlantic.dplabs-internal.com   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"<TOKEN_ADDRESS>","data":"0x70a08231<WALLET_ADDRESS_PADDED>"},"latest"],"id":1}'
```

### Step 4: Cross-reference with Safety Data

For each token found, check safety using the TokenSafetyRegistry (see token-data.md).

### Known Tokens on Pharos Testnet

| Token | Address | Decimals |
|---|---|---|
| PHAR | native | 18 |
| USDC | 0xcfC8330f4BCAB529c625D12781b1C19466A9Fc8B | 6 |
| USDT | 0xE7E84B8B4f39C507499c40B4ac199B050e2882d5 | 6 |
| WBTC | 0x0c64F03EEa5c30946D5c55B4b532D08ad74638a4 | 18 |
| WETH | 0x7d211F77525ea39A0592794f793cC1036eEaccD5 | 18 |
| WPHRS | 0x838800b758277CC111B2d48Ab01e5E164f8E9471 | 18 |
