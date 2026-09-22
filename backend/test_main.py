import pytest
from fastapi.testclient import TestClient
from main import app
from calculator import calculate_stock_profit

client = TestClient(app)

def test_calculator_logic_profit():
    res = calculate_stock_profit(
        shares=100,
        purchase_price=50.0,
        purchase_commission=10.0,
        sale_price=70.0,
        sale_commission=10.0
    )
    assert res.gross_purchase_cost == 5000.0
    assert res.net_cost_basis == 5010.0
    assert res.gross_sale_revenue == 7000.0
    assert res.net_proceeds == 6990.0
    assert res.total_commissions == 20.0
    assert res.net_profit_loss == 1980.0
    assert pytest.approx(res.roi_percent, 0.01) == 39.52
    assert pytest.approx(res.break_even_price, 0.01) == 50.20
    assert res.is_profit is True

def test_calculator_logic_loss():
    res = calculate_stock_profit(
        shares=50,
        purchase_price=100.0,
        purchase_commission=15.0,
        sale_price=80.0,
        sale_commission=15.0
    )
    # Gross cost: 50 * 100 = 5000; Net cost basis = 5015
    # Gross sale: 50 * 80 = 4000; Net proceeds = 3985
    # Net profit/loss: 3985 - 5015 = -1030
    assert res.net_cost_basis == 5015.0
    assert res.net_proceeds == 3985.0
    assert res.net_profit_loss == -1030.0
    assert pytest.approx(res.roi_percent, 0.01) == -20.54
    assert res.is_profit is False

def test_calculator_logic_zero_commission():
    res = calculate_stock_profit(
        shares=10,
        purchase_price=20.0,
        purchase_commission=0.0,
        sale_price=25.0,
        sale_commission=0.0
    )
    assert res.net_profit_loss == 50.0
    assert res.roi_percent == 25.0
    assert res.break_even_price == 20.0

def test_calculator_invalid_inputs():
    with pytest.raises(ValueError, match="Shares must be greater than zero"):
        calculate_stock_profit(0, 10, 0, 10, 0)
    
    with pytest.raises(ValueError, match="Prices cannot be negative"):
        calculate_stock_profit(10, -5, 0, 10, 0)

def test_api_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Stock Profit Calculator API"}

def test_api_calculate_endpoint():
    payload = {
        "shares": 100,
        "purchase_price": 50.0,
        "purchase_commission": 10.0,
        "sale_price": 70.0,
        "sale_commission": 10.0
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["net_profit_loss"] == 1980.0
    assert data["is_profit"] is True
    assert "Net Profit of $1,980.00" in data["message"]

def test_api_calculate_invalid_payload():
    payload = {
        "shares": -5,
        "purchase_price": 50.0,
        "purchase_commission": 10.0,
        "sale_price": 70.0,
        "sale_commission": 10.0
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)
