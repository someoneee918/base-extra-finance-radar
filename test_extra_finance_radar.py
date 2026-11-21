#!/usr/bin/env python3
"""
Unit Tests for Base Extra Finance Leveraged Yield Farming Radar
"""

import unittest
from extra_finance_radar import (
    calculate_lyf_position_yield,
    calculate_debt_ratio_and_liquidation,
    calculate_liquidator_profit,
    calculate_utilization_rate_model,
    generate_vip_sentinel_script,
    BASE_RECEIVE_ADDRESS,
    SOL_RECEIVE_ADDRESS
)

class TestExtraFinanceRadar(unittest.TestCase):

    def test_lyf_position_yield(self):
        # $10,000 equity, 3x leverage -> $30,000 position, $20,000 borrow
        # Pool APR 35% -> Gross $30k * 0.35 = $10,500
        # Borrow APR 12% -> Borrow cost $20k * 0.12 = $2,400
        # Net yield = $10,500 - $2,400 = $8,100
        # Net equity APR = 8,100 / 10,000 = 81.0%
        # Enhancement ratio = 81.0 / 35.0 = 2.31x
        res = calculate_lyf_position_yield(equity_usd=10000.0, leverage=3.0, pool_base_apr_pct=35.0, borrow_apr_pct=12.0)
        self.assertEqual(res["position_value_usd"], 30000.0)
        self.assertEqual(res["borrowed_amount_usd"], 20000.0)
        self.assertEqual(res["gross_yield_usd"], 10500.0)
        self.assertEqual(res["borrow_cost_usd"], 2400.0)
        self.assertEqual(res["net_yield_usd"], 8100.0)
        self.assertEqual(res["net_equity_apr_pct"], 81.0)
        self.assertEqual(res["yield_enhancement_ratio"], 2.31)
        self.assertTrue(res["has_positive_carry"])

    def test_debt_ratio_and_liquidation(self):
        # Case 1: Healthy position ($30k position, $20k debt -> 66.67% debt ratio vs 85% kill factor)
        healthy = calculate_debt_ratio_and_liquidation(30000.0, 20000.0, kill_factor_pct=85.0)
        self.assertAlmostEqual(healthy["debt_ratio_pct"], 66.67, places=1)
        self.assertFalse(healthy["is_liquidatable"])
        self.assertEqual(healthy["status"], "HEALTHY")
        self.assertAlmostEqual(healthy["safety_cushion_pct"], 18.33, places=1)
        
        # Case 2: Warning position ($25k position, $20.5k debt -> 82.0% debt ratio)
        warning = calculate_debt_ratio_and_liquidation(25000.0, 20500.0, kill_factor_pct=85.0)
        self.assertFalse(warning["is_liquidatable"])
        self.assertEqual(warning["status"], "WARNING")
        
        # Case 3: Liquidatable position ($23k position, $20k debt -> 86.96% debt ratio)
        liq = calculate_debt_ratio_and_liquidation(23000.0, 20000.0, kill_factor_pct=85.0)
        self.assertTrue(liq["is_liquidatable"])
        self.assertEqual(liq["status"], "LIQUIDATABLE")

    def test_liquidator_profit(self):
        # Debt: $10,000. Bonus: 5% = $500. Received collateral: $10,500.
        # Slippage: 0.5% on $10,500 = $52.50. Base gas: $0.02.
        # Net profit: $500 - $52.50 - $0.02 = $447.48.
        prof = calculate_liquidator_profit(
            debt_value_usd=10000.0,
            liquidation_bonus_pct=0.05,
            base_gas_usd=0.02,
            swap_slippage_pct=0.005
        )
        self.assertEqual(prof["gross_bonus_usd"], 500.0)
        self.assertEqual(prof["slippage_drag_usd"], 52.50)
        self.assertEqual(prof["net_profit_usd"], 447.48)
        self.assertTrue(prof["is_profitable"])

    def test_utilization_rate_model(self):
        # Normal (60% utilization <= 80% kink)
        # Base 2% + (60 / 80) * 10% = 2% + 7.5% = 9.5%
        normal = calculate_utilization_rate_model(600000.0, 1000000.0)
        self.assertEqual(normal["utilization_pct"], 60.0)
        self.assertFalse(normal["is_kinked"])
        self.assertEqual(normal["borrow_rate_pct"], 9.5)
        
        # Surged (90% utilization > 80% kink)
        # Excess = (90 - 80) / 20 = 0.50. Rate = 2% + 10% + 0.50 * 120% = 72.0%
        surged = calculate_utilization_rate_model(900000.0, 1000000.0)
        self.assertEqual(surged["utilization_pct"], 90.0)
        self.assertTrue(surged["is_kinked"])
        self.assertEqual(surged["borrow_rate_pct"], 72.0)

    def test_generate_vip_script(self):
        script = generate_vip_sentinel_script(BASE_RECEIVE_ADDRESS, SOL_RECEIVE_ADDRESS)
        self.assertIn("Extra Finance Sentinel", script)
        self.assertIn(BASE_RECEIVE_ADDRESS, script)
        self.assertIn(SOL_RECEIVE_ADDRESS, script)
        self.assertIn("EXTRA_FINANCE_VAULT", script)

if __name__ == "__main__":
    unittest.main()
