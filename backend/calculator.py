from dataclasses import dataclass

@dataclass
class StockCalculationResult:
    shares: float
    purchase_price: float
    purchase_commission: float
    sale_price: float
    sale_commission: float
    gross_purchase_cost: float
    net_cost_basis: float
    gross_sale_revenue: float
    net_proceeds: float
    total_commissions: float
    net_profit_loss: float
    roi_percent: float
    break_even_price: float
    is_profit: bool

def calculate_stock_profit(
    shares: float,
    purchase_price: float,
    purchase_commission: float,
    sale_price: float,
    sale_commission: float
) -> StockCalculationResult:
    """
    Calculate stock sale profit or loss and associated transaction metrics.
    """
    if shares <= 0:
        raise ValueError("Shares must be greater than zero.")
    if purchase_price < 0 or sale_price < 0:
        raise ValueError("Prices cannot be negative.")
    if purchase_commission < 0 or sale_commission < 0:
        raise ValueError("Commissions cannot be negative.")

    gross_purchase_cost = round(shares * purchase_price, 4)
    net_cost_basis = round(gross_purchase_cost + purchase_commission, 4)
    gross_sale_revenue = round(shares * sale_price, 4)
    net_proceeds = round(gross_sale_revenue - sale_commission, 4)
    total_commissions = round(purchase_commission + sale_commission, 4)
    net_profit_loss = round(net_proceeds - net_cost_basis, 4)
    
    roi_percent = round((net_profit_loss / net_cost_basis) * 100.0, 4) if net_cost_basis > 0 else 0.0
    break_even_price = round((net_cost_basis + sale_commission) / shares, 4)
    
    return StockCalculationResult(
        shares=shares,
        purchase_price=purchase_price,
        purchase_commission=purchase_commission,
        sale_price=sale_price,
        sale_commission=sale_commission,
        gross_purchase_cost=gross_purchase_cost,
        net_cost_basis=net_cost_basis,
        gross_sale_revenue=gross_sale_revenue,
        net_proceeds=net_proceeds,
        total_commissions=total_commissions,
        net_profit_loss=net_profit_loss,
        roi_percent=roi_percent,
        break_even_price=break_even_price,
        is_profit=net_profit_loss >= 0
    )
