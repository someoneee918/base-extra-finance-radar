#!/usr/bin/env python3
"""
Base Extra Finance Leveraged Yield Farming (LYF) & Lending Utilization Radar
============================================================================
Commercial DeFi intelligence engine analyzing:
1. Leveraged Yield Farming (LYF, up to 7x) Net Compounded Equity APY
2. Debt Ratio & Critical Kill Factor (85%) Liquidation Boundaries on Base L2
3. Isolated Lending Vault Kinked Utilization Curve & Borrow Rate Surges
4. Atomic Liquidator Debt Clearance & Base L2 Gas Clearance Economics
5. Non-Custodial VIP Sentinel License Generator (5 Base USDC / 0.03 SOL)
"""

from typing import Dict, Any

BASE_RECEIVE_ADDRESS = "0xF0E0D361bBE899F3089f0a968506eF2B97693c01"
SOL_RECEIVE_ADDRESS = "DW2MdHEq3qZ6nh9b5YFUoaPnBuuxC8Gz2785kwbbjSAM"

def calculate_lyf_position_yield(
    equity_usd: float,
    leverage: float,
    pool_base_apr_pct: float = 35.0,
    borrow_apr_pct: float = 12.0
) -> Dict[str, Any]:
    """
    Computes leveraged yield farming returns and debt financing costs:
    Position Value = Equity * Leverage
    Borrowed Amount = Equity * (Leverage - 1)
    Gross Yield = Position Value * Pool_Base_APR
    Borrow Interest = Borrowed Amount * Borrow_APR
    Net Yield = Gross Yield - Borrow Interest
    Net Equity APR = Net Yield / Equity
    """
    if equity_usd <= 0 or leverage < 1.0 or pool_base_apr_pct < 0 or borrow_apr_pct < 0:
        raise ValueError("Invalid parameters.")
        
    position_value_usd = equity_usd * leverage
    borrowed_amount_usd = equity_usd * (leverage - 1.0)
    
    gross_yield_usd = position_value_usd * (pool_base_apr_pct / 100.0)
    borrow_cost_usd = borrowed_amount_usd * (borrow_apr_pct / 100.0)
    net_yield_usd = gross_yield_usd - borrow_cost_usd
    
    net_equity_apr_pct = (net_yield_usd / equity_usd) * 100.0
    yield_enhancement_ratio = net_equity_apr_pct / pool_base_apr_pct if pool_base_apr_pct > 0 else 0.0
    
    return {
        "equity_usd": equity_usd,
        "leverage": leverage,
        "position_value_usd": round(position_value_usd, 2),
        "borrowed_amount_usd": round(borrowed_amount_usd, 2),
        "gross_yield_usd": round(gross_yield_usd, 2),
        "borrow_cost_usd": round(borrow_cost_usd, 2),
        "net_yield_usd": round(net_yield_usd, 2),
        "net_equity_apr_pct": round(net_equity_apr_pct, 2),
        "yield_enhancement_ratio": round(yield_enhancement_ratio, 2),
        "has_positive_carry": net_yield_usd > 0
    }

def calculate_debt_ratio_and_liquidation(
    position_value_usd: float,
    debt_value_usd: float,
    kill_factor_pct: float = 85.0
) -> Dict[str, Any]:
    """
    Computes debt ratio and liquidation safety cushion:
    Debt Ratio = (Debt Value / Position Value) * 100
    Safety Cushion = Kill Factor - Debt Ratio
    If Debt Ratio >= Kill Factor, position is liquidatable.
    """
    if position_value_usd <= 0 or debt_value_usd < 0:
        raise ValueError("Invalid values.")
        
    debt_ratio_pct = (debt_value_usd / position_value_usd) * 100.0
    safety_cushion_pct = max(0.0, kill_factor_pct - debt_ratio_pct)
    
    is_liquidatable = debt_ratio_pct >= kill_factor_pct
    status = "LIQUIDATABLE" if is_liquidatable else (
        "WARNING" if debt_ratio_pct >= (kill_factor_pct - 5.0) else "HEALTHY"
    )
    
    return {
        "position_value_usd": position_value_usd,
        "debt_value_usd": debt_value_usd,
        "debt_ratio_pct": round(debt_ratio_pct, 2),
        "kill_factor_pct": kill_factor_pct,
        "safety_cushion_pct": round(safety_cushion_pct, 2),
        "is_liquidatable": is_liquidatable,
        "status": status
    }

def calculate_liquidator_profit(
    debt_value_usd: float,
    liquidation_bonus_pct: float = 0.05,
    base_gas_usd: float = 0.02,
    swap_slippage_pct: float = 0.005
) -> Dict[str, Any]:
    """
    Calculates net reward for liquidating an unhealthy Extra Finance position:
    Gross Bonus = Debt * Liquidation_Bonus
    Slippage Drag = Debt * (1 + Bonus) * Slippage
    Net Profit = Gross Bonus - Slippage Drag - Base_Gas
    """
    if debt_value_usd <= 0 or liquidation_bonus_pct <= 0:
        raise ValueError("Invalid parameters.")
        
    gross_bonus_usd = debt_value_usd * liquidation_bonus_pct
    received_collateral_usd = debt_value_usd * (1.0 + liquidation_bonus_pct)
    slippage_drag_usd = received_collateral_usd * swap_slippage_pct
    net_profit_usd = max(0.0, gross_bonus_usd - slippage_drag_usd - base_gas_usd)
    
    return {
        "debt_value_usd": debt_value_usd,
        "gross_bonus_usd": round(gross_bonus_usd, 2),
        "slippage_drag_usd": round(slippage_drag_usd, 2),
        "base_gas_usd": base_gas_usd,
        "net_profit_usd": round(net_profit_usd, 2),
        "is_profitable": net_profit_usd > 1.0
    }

def calculate_utilization_rate_model(
    total_borrowed_usd: float,
    total_supplied_usd: float,
    kink_pct: float = 80.0,
    base_rate_pct: float = 2.0,
    slope1_pct: float = 10.0,
    slope2_pct: float = 120.0
) -> Dict[str, Any]:
    """
    Kinked borrow rate model for Extra Finance lending vaults.
    """
    if total_supplied_usd <= 0 or total_borrowed_usd < 0:
        raise ValueError("Invalid supplied or borrowed amount.")
        
    utilization_pct = min(100.0, (total_borrowed_usd / total_supplied_usd) * 100.0)
    
    if utilization_pct <= kink_pct:
        borrow_rate_pct = base_rate_pct + (utilization_pct / kink_pct) * slope1_pct
    else:
        excess_pct = (utilization_pct - kink_pct) / (100.0 - kink_pct)
        borrow_rate_pct = base_rate_pct + slope1_pct + (excess_pct * slope2_pct)
        
    return {
        "total_borrowed_usd": total_borrowed_usd,
        "total_supplied_usd": total_supplied_usd,
        "utilization_pct": round(utilization_pct, 2),
        "kink_pct": kink_pct,
        "borrow_rate_pct": round(borrow_rate_pct, 2),
        "is_kinked": utilization_pct > kink_pct
    }

def generate_vip_sentinel_script(
    base_wallet: str = BASE_RECEIVE_ADDRESS,
    sol_wallet: str = SOL_RECEIVE_ADDRESS
) -> str:
    """
    Generates TypeScript Extra Finance LYF debt ratio sentinel script.
    """
    return f"""// Base Extra Finance LYF Position Health & Debt Ratio Sentinel
// VIP License Unlocked for {base_wallet} (Base) / {sol_wallet} (Solana)
import {{ ethers }} from 'ethers';

const BASE_RPC = process.env.BASE_RPC_URL || 'https://mainnet.base.org';
const EXTRA_FINANCE_VAULT = '0x1234567890123456789012345678901234567890';

export async function monitorLyfPosition(positionId: number) {{
    const provider = new ethers.JsonRpcProvider(BASE_RPC);
    console.log(`[Extra Finance Sentinel] Querying position #${{positionId}} debt ratio...`);
    // Connect to Extra Finance Position Manager contract
    // When debt ratio exceeds 80% (within 5% of kill factor), trigger alert or automated partial deleverage
}}
"""
