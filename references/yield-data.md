# Yield Data — Pharos Atlantic Testnet

## Registered Protocols

The following protocols are registered on the YieldRegistry (0x6c65B773e1250D40e5902615FDd33d054C455ede):

### Protocol 1: Centrifuge (Lending)
- **Category:** Lending
- **Pair:** PHAR/USDC
- **APY:** 24.65%
- **TVL:** $1,200,000
- **Risk:** LOW
- **Verified:** Yes
- **Fresh:** Yes (< 24h)

### Protocol 2: Ember (DEX)
- **Category:** DEX
- **Pair:** PHAR/ETH
- **APY:** 18.30%
- **TVL:** $850,000
- **Risk:** MEDIUM
- **Verified:** Yes
- **Fresh:** Yes (< 24h)

### Protocol 3: Avalon (Yield)
- **Category:** Yield
- **Pair:** USDC/USDT
- **APY:** 12.50%
- **TVL:** $2,500,000
- **Risk:** LOW
- **Verified:** Yes
- **Fresh:** Yes (< 24h)

### Protocol 4: PharosSwap (DEX)
- **Category:** DEX
- **Pair:** WETH/PHAR
- **APY:** 45.20%
- **TVL:** $320,000
- **Risk:** HIGH
- **Verified:** No
- **Fresh:** Yes (< 24h)

### Protocol 5: StableYield (Yield)
- **Category:** Yield
- **Pair:** USDC
- **APY:** 8.75%
- **TVL:** $5,000,000
- **Risk:** LOW
- **Verified:** Yes
- **Fresh:** Yes (< 24h)

---

## How to Verify Live Data

To query the YieldRegistry directly via JSON-RPC:

```bash
# Get all registered protocols
curl -s -X POST https://atlantic.dplabs-internal.com   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0x741c53eb"},"latest"],"id":1}'

# Get latest yield for a specific protocol
curl -s -X POST https://atlantic.dplabs-internal.com   -H "Content-Type: application/json"   -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0xc2f8608d<PROTOCOL_ADDRESS_PADDED>"},"latest"],"id":1}'
```

**Note:** APY is in basis points in the contract (100 = 1%, 5000 = 50%). The values above are pre-converted to percentages.
