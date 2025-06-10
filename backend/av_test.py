"""
av_test.py

Test script for Alpha Vantage API:
- Fetches latest daily close price (TIME_SERIES_DAILY)
- Fetches company overview (OVERVIEW)

Usage:
  $ pip install requests python-dotenv
  $ export ALPHA_VANTAGE_API_KEY=your_key    # or place in .env
  $ python av_test.py
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load API key from .env or environment
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    print("Error: ALPHA_VANTAGE_API_KEY not set in environment or .env")
    sys.exit(1)

BASE_URL = "https://www.alphavantage.co/query"


def get_json(params: dict) -> dict:
    """
    Helper to call Alpha Vantage with given params and return JSON.
    """
    response = requests.get(BASE_URL, params=params)
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        print(f"HTTP error for params {params}: {e}")
        return {}
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return {}


def get_daily_close(symbol: str):
    """
    Fetch the most recent daily closing price for a symbol.
    Returns (date_str, price_float) or (None, None) on error.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    data = get_json(params)
    ts = data.get("Time Series (Daily)")
    if not ts:
        print(f"Error fetching daily series for {symbol}: {data.get('Note') or data}")
        return None, None
    latest_date = next(iter(ts))
    price = ts[latest_date]["4. close"]
    return latest_date, float(price)


def get_company_overview(symbol: str) -> dict:
    """
    Fetch company overview data for a symbol.
    Returns a dict of selected fields.
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY
    }
    data = get_json(params)
    if not data or 'Symbol' not in data:
        print(f"Error fetching overview for {symbol}: {data.get('Note') or data}")
        return {}

    # Extract key fields
    keys = [
        "Symbol", "Name", "EPS", "BookValue", "PERatio",
        "MarketCapitalization", "ReturnOnEquityTTM", "DebtToEquity"
    ]
    return {k: data.get(k) for k in keys}


def main():
    symbol = input("Enter stock symbol (e.g. AAPL): ").strip().upper()

    # Daily close
    date, price = get_daily_close(symbol)
    if date:
        print(f"Latest close for {symbol} on {date} is ${price:.2f}")

    # Company overview
    overview = get_company_overview(symbol)
    if overview:
        print("\nCompany Overview:")
        for key, val in overview.items():
            print(f"  {key}: {val}")


if __name__ == "__main__":
    main()