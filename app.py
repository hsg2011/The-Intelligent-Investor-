import sqlite3
import math
from dotenv import load_dotenv
from analyze_stock import analyze_stock_combined
import pandas as pd
import yfinance as yf

# load env var from .env
load_dotenv()

# Function to insert stock data into database
def insert_stock_data(symbol, price, pe_ratio, market_cap, recommendation):
    # connect to database
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    # Insert data into stocks table
    cursor.execute(''' 
                   INSERT INTO stocks (symbol, price, pe_ratio, market_cap, recommendation)
                   VALUES (?,?,?,?,?) 
                   ''', (symbol, price, pe_ratio, market_cap, recommendation))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Get financial data using yfinance
def fetch_financials(symbol):
    stock = yf.Ticker(symbol)
    # Fetch key financial data
    pe_ratio = stock.info.get('forwardPE')  # You could also try 'trailingPE'
    market_cap = stock.info.get('marketCap')  # Market cap
    stock_price = stock.info.get('regularMarketPrice')  # Current stock price

    # Data for Graham number calculation
    eps = stock.info.get('trailingEps')    # Earnings Per Share
    bvps = stock.info.get('bookValue')       # Book Value Per Share

    if stock_price is None:
        stock_history = stock.history(period="1d")
        stock_price = stock_history['Close'].iloc[-1] if not stock_history.empty else None

    return pe_ratio, market_cap, stock_price, eps, bvps

# Get S&P 500 symbols from Wikipedia
def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url)[0]
    # Uncomment below to check the columns if needed:
    # print(f"Columns in the S&P 500 table: {sp500_table.columns}")
    return sp500_table['Symbol'].tolist()  # Fetching symbols from the table

if __name__ == '__main__':
    sp500_symbols = get_sp500_symbols()

    for stock_symbol in sp500_symbols[:5]:  # Testing with first 5 symbols
        try:
            pe_ratio, market_cap, stock_price, eps, bvps, roe, debt_to_equity = fetch_financials(stock_symbol)
            
            # Get the combined recommendation
            recommendation = analyze_stock_combined(stock_symbol, stock_price, pe_ratio, market_cap, eps, bvps, roe, debt_to_equity)
            
            # Insert the fetched data into the database
            insert_stock_data(stock_symbol, stock_price, pe_ratio, market_cap, recommendation)
            
            print(f"{stock_symbol}: Price = {stock_price}, PE Ratio = {pe_ratio}, Market Cap = {market_cap}")
            print(f"Recommendation: {recommendation}")
        except Exception as e:
            print(f"Error fetching data for {stock_symbol}: {e}")
