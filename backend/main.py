from fastapi import FastAPI, HTTPException
from data import update_sp500_symbols, get_sp500_symbols
from analysis import analyze_stock_combined
from plotting import plot_price, plot_pe
from db_setup import init_db
from app import fetch_financials  # reuse your cleaned function from app.py
import logging
from db import get_latest_stock_record

app = FastAPI(title="Stock Analysis API")

@app.on_event("startup")
def startup_event():
    # Initialize DB and update symbols
    init_db()
    update_sp500_symbols()

@app.get("/symbols")
def symbols():
    return get_sp500_symbols()


@app.get("/record/{symbol}")
def read_record(symbol: str):
    """
    Returns the latest analysis record for SYMBOL from the local database.
    """
    rec = get_latest_stock_record(symbol)
    if not rec:
        raise HTTPException(status_code=404, detail=f"No record found for {symbol}")
    return rec

# configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    symbol = symbol.upper()
    try:
        price, pe, mc, eps, bvps, roe, de = fetch_financials(symbol)
    except Exception as e:
        logger.exception(f"Error fetching financials for {symbol}")
        raise HTTPException(status_code=502, detail="Upstream data fetch error")

    # Check minimum data
    if price is None or eps is None or bvps is None:
        logger.warning(f"Incomplete data for {symbol}: price={price}, eps={eps}, bvps={bvps}")
        raise HTTPException(status_code=404, detail=f"Incomplete data for {symbol}")

    try:
        rec = analyze_stock_combined(symbol, price, pe, mc, eps, bvps, roe or 0.0, de or 0.0)
    except Exception as e:
        logger.exception(f"Error analyzing stock for {symbol}")
        raise HTTPException(status_code=500, detail="Analysis failure")

    return {"symbol": symbol, "recommendation": rec}


@app.get("/plot/price/{symbol}")
async def get_price_plot(symbol: str):
    return plot_price(symbol)

@app.get("/plot/pe/{symbol}")
async def get_pe_plot(symbol: str):
    return plot_pe(symbol)