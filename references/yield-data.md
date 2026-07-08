# Yield Data — Pharos Atlantic Testnet

**Source:** On-chain YieldRegistry (0x6c65B773e1250D40e5902615FDd33d054C455ede)
**Chain ID:** 688689
**Last updated:** Live from chain

## Registered Protocols: 9
## Protocols with Yield Data: 8

---

## Yield Opportunities (Ranked by APY)

### #1 PharVault (Yield)
- **Pair:** Auto-compound
- **APY:** 65.00%
- **TVL:** $800,000
- **Risk:** HIGH
- **Reporter:** 0x8919...8061

### #2 PharSwap (DEX)
- **Pair:** PHAR/USDC
- **APY:** 45.00%
- **TVL:** $500,000
- **Risk:** MEDIUM
- **Reporter:** 0x8919...8061

### #3 PharSwap (DEX)
- **Pair:** PHAR/ETH
- **APY:** 32.00%
- **TVL:** $1,500,000
- **Risk:** MEDIUM
- **Reporter:** 0x8919...8061

### #4 PharStake (Staking)
- **Pair:** PHAR Staking
- **APY:** 25.00%
- **TVL:** $3,000,000
- **Risk:** LOW
- **Reporter:** 0x8919...8061

### #5 PharLend (Lending)
- **Pair:** USDC Supply
- **APY:** 12.00%
- **TVL:** $500,000
- **Risk:** LOW
- **Reporter:** 0x8919...8061

### #6 Ember Protocol (Yield)
- **Pair:** SUI
- **APY:** 7.82%
- **TVL:** $5,270,000
- **Risk:** MEDIUM
- **Reporter:** 0x8919...8061

### #7 Centrifuge Protocol (RWA)
- **Pair:** USDC
- **APY:** 5.35%
- **TVL:** $15,100,000
- **Risk:** LOW
- **Reporter:** 0x8919...8061

### #8 Avalon Finance (Lending)
- **Pair:** XSOLVBTC
- **APY:** 1.00%
- **TVL:** $100,000
- **Risk:** LOW
- **Reporter:** 0x8919...8061

---

## No Yield Data

### FaroSwap (DEX) — Registered but no yield reported yet

---

## How to Verify Live Data

```bash
# Get all registered protocols
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0x741c53eb"},"latest"],"id":1}'

# Get latest yield for a protocol (getLatestYield selector: 0xc2f8608d)
curl -s -X POST https://atlantic.dplabs-internal.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x6c65B773e1250D40e5902615FDd33d054C455ede","data":"0xc2f8608d<PROTOCOL_ADDRESS_PADDED>"},"latest"],"id":1}'
```

**Note:** APY is stored in basis points in the contract (100 = 1%, 5000 = 50%). Values above are pre-converted to percentages.
