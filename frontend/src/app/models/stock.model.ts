export interface StockCalculationRequest {
  shares: number;
  purchase_price: number;
  purchase_commission: number;
  sale_price: number;
  sale_commission: number;
}

export interface StockCalculationResponse {
  shares: number;
  purchase_price: number;
  purchase_commission: number;
  sale_price: number;
  sale_commission: number;
  gross_purchase_cost: number;
  net_cost_basis: number;
  gross_sale_revenue: number;
  net_proceeds: number;
  total_commissions: number;
  net_profit_loss: number;
  roi_percent: number;
  break_even_price: number;
  is_profit: boolean;
  message: string;
}
