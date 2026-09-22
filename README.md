<img width="899" height="861" alt="Screenshot 2026-09-22 at 12 21 57 AM" src="https://github.com/user-attachments/assets/5ccd5407-ea6a-4b1b-8f24-626cda4250f3" />

<img width="912" height="855" alt="Screenshot 2026-09-22 at 12 22 34 AM" src="https://github.com/user-attachments/assets/6ec4c980-b0b9-4c4b-a118-f99b4588f06a" />



# Stock Profit & Loss Calculator 📊

A full-stack web application built with **Angular 22** on the frontend and **Python FastAPI** on the backend. The application calculates stock transaction metrics including Net Profit/Loss, Return on Investment (ROI %), Cost Basis, Net Proceeds, Total Commissions, and Break-Even Sale Price per share.

![Stock Profit Calculator](https://img.shields.io/badge/Angular-22-red?style=flat&logo=angular)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)

## 🌟 Key Features

- **Interactive Inputs**: Number of shares, purchase price, purchase commission, sale price, and sale commission.
- **Real-Time Validation**: Instant form validation preventing invalid inputs ($> 0$ for shares, $\ge 0$ for prices and commissions).
- **Quick Preset Scenarios**: Pre-configured buttons for *Profitable Trade*, *Loss Trade*, *Break-Even Trade*, and *High Volume Tech Stock*.
- **Comprehensive Financial Metrics**:
  - Net Profit / Loss ($)
  - Return on Investment (ROI %)
  - Target Break-Even Sale Price ($/share)
  - Net Cost Basis vs Gross Purchase Cost
  - Net Proceeds vs Gross Sale Revenue
  - Total Commissions Paid
- **Visual Outcome Highlights**: Dynamic color-coded banners (Green for profit, Red for loss, Amber for break-even).

---

## 📐 Financial Calculation Engine

Given:
- $N$ = Number of shares (`shares`)
- $P_{buy}$ = Purchase price per share (`purchase_price`)
- $C_{buy}$ = Commission paid on purchase (`purchase_commission`)
- $P_{sell}$ = Sale price per share (`sale_price`)
- $C_{sell}$ = Commission paid on sale (`sale_commission`)

Calculated Metrics:
$$\text{Net Cost Basis} = (N \times P_{buy}) + C_{buy}$$
$$\text{Net Proceeds} = (N \times P_{sell}) - C_{sell}$$
$$\text{Net Profit / Loss} = \text{Net Proceeds} - \text{Net Cost Basis}$$
$$\text{ROI \%} = \frac{\text{Net Profit / Loss}}{\text{Net Cost Basis}} \times 100\%$$
$$\text{Break-Even Price} = \frac{\text{Net Cost Basis} + C_{sell}}{N}$$

---

## 🛠️ Project Structure

```
stock-profit-calculator/
├── backend/
│   ├── calculator.py       # Core calculation engine
│   ├── main.py             # FastAPI app endpoints & CORS middleware
│   ├── test_main.py        # Pytest test suite (7 tests)
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── models/     # Stock calculation interfaces
    │   │   ├── services/   # Angular HttpClient service with fallback
    │   │   ├── app.component.ts
    │   │   ├── app.component.html
    │   │   └── app.component.css
    │   └── main.ts
    ├── package.json
    ├── angular.json
    └── tsconfig.json
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8050 --reload
```

The API docs will be available at [http://localhost:8050/docs](http://localhost:8050/docs).

### 2. Frontend Setup (Angular)

```bash
cd frontend
npm install
npm start
```

Open [http://localhost:4200](http://localhost:4200) in your browser.

---

## 🧪 Running Tests

### Backend Unit & Integration Tests

```bash
cd backend
./venv/bin/pytest test_main.py
```

---

## 📄 License

MIT License
