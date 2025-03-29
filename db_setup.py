import sqlite3

#create database
conn = sqlite3.connect('stocks.db')

cursor = conn.cursor()

# create table for stock data
# stock factors such as symbol, price, PE ratio, market cap, last time updated
cursor.execute(''' 
               CREATE TABLE IF NOT EXISTS stocks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               symbol TEXT NOT NULL,
               price REAL,
               pe_ratio REAL,
               market_cap REAL,
               recommendation TEXT,
               last_updated DATETIME DEFAULT CURRENT_TIMESTAMP)
               ''')

# Create table for S&P 500 symbols
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sp500_symbols (
        symbol TEXT PRIMARY KEY
    )
''')

conn.commit()
conn.close()

print("database updated")