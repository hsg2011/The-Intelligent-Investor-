import requests
import sqlite3
import os 
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf

# load env var form .env
load_dotenv()

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
BASE_URL = 'https://www.alphavantage.co/query'

# # Fetch stock data from alpha vantage api
# def fetch_stock_price(symbol):
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'
#     response = requests.get(url)
#     data = response.json()

#     if 'Time Series (Daily)' in data:
#         latest_day = list(data['Time Series (Daily)'].keys())[0]
#         stock_price = float(data['Time Series (Daily)'][latest_day]['4. close'])
#         return stock_price
#     else:
#         print(f"Error: 'Time Series (Daily)' data not found for {symbol}. Response: {data}")
#         return None



# Function to insert stock data into database
def insert_stock_data(symbol, price, pe_ratio, market_cap):
    # connect to database
    conn = sqlite3.connect('stocks.db')
    cursor= conn.cursor()

    #insert data into stocks table
    cursor.execute(''' 
                   INSERT INTO stocks (symbol, price, pe_ratio, market_cap)
                   VALUES (?,?,?,?) 
                   ''', (symbol, price, pe_ratio, market_cap))
    
    # commit changes and close connection
    conn.commit()
    conn.close()

# Get financial data using yfinance
def fetch_financials(symbol):
    stock = yf.Ticker(symbol)
    # Fetch key financial data
    pe_ratio = stock.info.get('forwardPE')  # PE ratio
    market_cap = stock.info.get('marketCap')  # Market cap
    stock_price = stock.info.get('regularMarketPrice')  # Current stock price

    if stock_price is None:
        stock_history = stock.history(period="1d")
        stock_price = stock_history['Close'].iloc[-1] if not stock_history.empty else None
        
    return pe_ratio, market_cap, stock_price


# Get S&P 500 symbols from yfinance
def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url)[0]
    #print(f"Columns in the S&P 500 table: {sp500_table.columns}")
    return sp500_table['Symbol'].tolist()  # Fetching symbols from the table

    
#Main 
if __name__ == '__main__':

    sp500_symbols = get_sp500_symbols()

    for stock_symbol in sp500_symbols[:5]:  # Limit to first 5 for testing
        try:
            pe_ratio, market_cap, stock_price = fetch_financials(stock_symbol)
            print(f"{stock_symbol}: PE Ratio = {pe_ratio}, Market Cap = {market_cap}, Stock Price = {stock_price}")
            # Insert the fetched data into the database
            insert_stock_data(stock_symbol, stock_price, pe_ratio, market_cap)
        except Exception as e:
            print(f"Error fetching data for {stock_symbol}: {e}")

        