import os
import requests
from dotenv import load_dotenv
from json import JSONDecodeError

# Load Alpha Vantage API key from .env or environment
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def get_json(params: dict) -> dict:
    """
    Internal helper to call Alpha Vantage and parse JSON safely.
    """
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    try:
        return response.json()
    except JSONDecodeError:
        return {}


def get_daily_close(symbol: str) -> (str, float):
    """
    Fetch the most recent daily closing price for a symbol.
    Returns (date_str, price) or (None, None).
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    data = get_json(params)
    ts = data.get("Time Series (Daily)")
    if not ts:
        return None, None
    latest_date = next(iter(ts))
    price = float(ts[latest_date]["4. close"])
    return latest_date, price


def fetch_financials(symbol: str):
    """
    Fetch core financial metrics for a given symbol from Alpha Vantage:
    - price (latest close)
    - P/E ratio
    - market capitalization
    - EPS
    - book value per share
    - return on equity (TTM)
    - debt-to-equity ratio
    Returns a tuple of floats or None for missing values.
    """
    sym = symbol.upper()

    # 1) Company overview
    overview_params = {
        "function": "OVERVIEW",
        "symbol": sym,
        "apikey": API_KEY
    }
    overview = get_json(overview_params)
    if not overview or overview.get("Symbol") != sym:
        # Unable to fetch company overview
        return None, None, None, None, None, None, None

    # 2) Latest closing price
    _, price = get_daily_close(sym)

    # 3) Extract and convert financial fields
    def to_float(key):
        try:
            val = overview.get(key)
            return float(val) if val is not None else None
        except (ValueError, TypeError):
            return None

    pe_ratio = to_float("PERatio")
    market_cap = to_float("MarketCapitalization")
    eps = to_float("EPS")
    bvps = to_float("BookValue")
    roe = to_float("ReturnOnEquityTTM")
    debt_to_equity = to_float("DebtToEquity")

    return price, pe_ratio, market_cap, eps, bvps, roe, debt_to_equity
