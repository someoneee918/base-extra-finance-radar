# Base Extra Finance Leveraged Yield Farming (LYF) & Lending Radar

[![Python Unit Tests](https://img.shields.io/badge/Unit%20Tests-5%2F5%20Passing-brightgreen.svg)]()
[![Base L2](https://img.shields.io/badge/Network-Base%20Mainnet-blue.svg)]()
[![Extra Finance](https://img.shields.io/badge/Protocol-Extra%20Finance-emerald.svg)]()
[![Live Visualizer](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-blue.svg)](https://someoneee918.github.io/base-extra-finance-radar/)

Commercial DeFi intelligence engine analyzing:
1. **Leveraged Yield Farming (LYF, up to 7x) Net Compounded Equity APY on Base L2**
2. **Debt Ratio & Critical Kill Factor (85.0%) Liquidation Boundaries**
3. **Isolated Lending Vault Kinked Utilization Curve & Borrow Rate Surges**
4. **Atomic Liquidator Debt Clearance & Base L2 Gas Clearance Economics**
5. **Non-Custodial VIP Sentinel License Generator (5 Base USDC / 0.03 SOL)**

---

## Live Interactive Dashboard
🌐 **Access the live dashboard at**: [https://someoneee918.github.io/base-extra-finance-radar/](https://someoneee918.github.io/base-extra-finance-radar/)

---

## Key Mathematical Models

### 1. Leveraged Yield Farming Net APY
$$\text{Position Value} = \text{Equity} \times L$$
$$\text{Borrowed Debt} = \text{Equity} \times (L - 1)$$
$$\text{APR}_{equity} = L \times \text{APR}_{pool} - (L - 1) \times R_{borrow}$$

For $\text{Equity} = \$10,000$, $L = 3.0\text{x}$, $\text{APR}_{pool} = 35.00\%$, and $R_{borrow} = 12.00\%$:
- Position Size: $\$30,000\text{ USD}$
- Borrowed Debt: $\$20,000\text{ USD}$
- **Net Compounded Equity APR: $+81.00\%\text{ APR}$ ($2.31\text{x}$ yield multiplier).**

### 2. Debt Ratio & Liquidation Kill Factor
$$\text{Debt Ratio} = \frac{\text{Debt Value}}{\text{Position Value}} \times 100\%$$
$$\text{Safety Cushion} = \text{Kill Factor} - \text{Debt Ratio}$$

When $\text{Debt Ratio} \ge 85.0\%$, the position is subject to atomic liquidation.

---

## Unit Test Verification
Run the 5/5 unit test suite:
```bash
python3 -m unittest test_extra_finance_radar.py
```

---

## Non-Custodial VIP Sentinel License
Unlock automated ethers.js LYF position health guardian and debt ratio monitor scripts by sending **5 Base USDC** or **0.03 SOL** to our verified receive addresses:
- **Base EVM:** `0xF0E0D361bBE899F3089f0a968506eF2B97693c01`
- **Solana:** `DW2MdHEq3qZ6nh9b5YFUoaPnBuuxC8Gz2785kwbbjSAM`
