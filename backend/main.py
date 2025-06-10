from fastapi import FastAPI, HTTPException
from data import update_sp500_symbols, get_sp500_symbols
from analysis import analyze_stock_combined
from plotting import plot_price, plot_pe
from db_setup import init_db
from app import fetch_financials  # reuse your cleaned function from app.py

app = FastAPI(title="Stock Analysis API")

@app.on_event("startup")
def startup_event():
    # Initialize DB and update symbols
    init_db()
    update_sp500_symbols()

@app.get("/symbols")
def symbols():
    return get_sp500_symbols()

@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    data = fetch_financials(symbol)
    if any(v is None for v in data):
        raise HTTPException(status_code=404, detail="Data not found")
    rec = analyze_stock_combined(symbol, *data)
    return {"symbol": symbol, "recommendation": rec}

@app.get("/plot/price/{symbol}")
async def get_price_plot(symbol: str):
    return plot_price(symbol)

@app.get("/plot/pe/{symbol}")
async def get_pe_plot(symbol: str):
    return plot_pe(symbol)