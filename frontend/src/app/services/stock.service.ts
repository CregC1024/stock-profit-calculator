import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of } from 'rxjs';
import { StockCalculationRequest, StockCalculationResponse } from '../models/stock.model';

@Injectable({
  providedIn: 'root'
})
export class StockService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8050/api';

  calculate(request: StockCalculationRequest): Observable<StockCalculationResponse> {
    return this.http.post<StockCalculationResponse>(`${this.apiUrl}/calculate`, request).pipe(
      catchError((error) => {
        console.warn('Backend API unavailable or error occurred, using client-side calculation engine fallback', error);
        return of(this.calculateClientSideFallback(request));
      })
    );
  }

  private calculateClientSideFallback(req: StockCalculationRequest): StockCalculationResponse {
    const grossPurchaseCost = Number((req.shares * req.purchase_price).toFixed(4));
    const netCostBasis = Number((grossPurchaseCost + req.purchase_commission).toFixed(4));
    const grossSaleRevenue = Number((req.shares * req.sale_price).toFixed(4));
    const netProceeds = Number((grossSaleRevenue - req.sale_commission).toFixed(4));
    const totalCommissions = Number((req.purchase_commission + req.sale_commission).toFixed(4));
    const netProfitLoss = Number((netProceeds - netCostBasis).toFixed(4));
    const roiPercent = netCostBasis > 0 ? Number(((netProfitLoss / netCostBasis) * 100).toFixed(4)) : 0;
    const breakEvenPrice = Number(((netCostBasis + req.sale_commission) / req.shares).toFixed(4));
    const isProfit = netProfitLoss >= 0;

    let message = '';
    if (netProfitLoss > 0) {
      message = `Net Profit of $${netProfitLoss.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} (${roiPercent >= 0 ? '+' : ''}${roiPercent.toFixed(2)}% ROI)`;
    } else if (netProfitLoss < 0) {
      message = `Net Loss of $${Math.abs(netProfitLoss).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} (${roiPercent.toFixed(2)}% ROI)`;
    } else {
      message = 'Transaction broke even ($0.00 profit/loss)';
    }

    return {
      shares: req.shares,
      purchase_price: req.purchase_price,
      purchase_commission: req.purchase_commission,
      sale_price: req.sale_price,
      sale_commission: req.sale_commission,
      gross_purchase_cost: grossPurchaseCost,
      net_cost_basis: netCostBasis,
      gross_sale_revenue: grossSaleRevenue,
      net_proceeds: netProceeds,
      total_commissions: totalCommissions,
      net_profit_loss: netProfitLoss,
      roi_percent: roiPercent,
      break_even_price: breakEvenPrice,
      is_profit: isProfit,
      message: message
    };
  }
}
