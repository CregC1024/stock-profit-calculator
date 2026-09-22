from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from calculator import calculate_stock_profit, StockCalculationResult

app = FastAPI(
    title="Stock Profit & Loss Calculator API",
    description="API for calculating stock investment profit, loss, ROI, and break-even metrics.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockCalculationRequest(BaseModel):
    shares: float = Field(..., gt=0, description="Number of shares traded (must be > 0)")
    purchase_price: float = Field(..., ge=0, description="Purchase price per share (must be >= 0)")
    purchase_commission: float = Field(0.0, ge=0, description="Commission paid on purchase (must be >= 0)")
    sale_price: float = Field(..., ge=0, description="Sale price per share (must be >= 0)")
    sale_commission: float = Field(0.0, ge=0, description="Commission paid on sale (must be >= 0)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "shares": 100.0,
                "purchase_price": 50.0,
                "purchase_commission": 10.0,
                "sale_price": 70.0,
                "sale_commission": 10.0
            }
        }
    }

class StockCalculationResponse(BaseModel):
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
    message: str

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Stock Profit Calculator API"}

@app.post("/api/calculate", response_model=StockCalculationResponse)
def calculate_profit(payload: StockCalculationRequest):
    try:
        res = calculate_stock_profit(
            shares=payload.shares,
            purchase_price=payload.purchase_price,
            purchase_commission=payload.purchase_commission,
            sale_price=payload.sale_price,
            sale_commission=payload.sale_commission
        )
        
        if res.net_profit_loss > 0:
            msg = f"Net Profit of ${res.net_profit_loss:,.2f} ({res.roi_percent:+.2f}% ROI)"
        elif res.net_profit_loss < 0:
            msg = f"Net Loss of ${abs(res.net_profit_loss):,.2f} ({res.roi_percent:+.2f}% ROI)"
        else:
            msg = "Transaction broke even ($0.00 profit/loss)"

        return StockCalculationResponse(
            shares=res.shares,
            purchase_price=res.purchase_price,
            purchase_commission=res.purchase_commission,
            sale_price=res.sale_price,
            sale_commission=res.sale_commission,
            gross_purchase_cost=res.gross_purchase_cost,
            net_cost_basis=res.net_cost_basis,
            gross_sale_revenue=res.gross_sale_revenue,
            net_proceeds=res.net_proceeds,
            total_commissions=res.total_commissions,
            net_profit_loss=res.net_profit_loss,
            roi_percent=res.roi_percent,
            break_even_price=res.break_even_price,
            is_profit=res.is_profit,
            message=msg
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
