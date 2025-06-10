import sqlite3

# Create or connect to SQLite database
def init_db(db_path: str = "stocks.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table for S&P 500 symbols\    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sp500_symbols (
        symbol TEXT PRIMARY KEY
    )
    ''')

    # Table for stocks and analysis results
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price REAL,
        pe_ratio REAL,
        market_cap REAL,
        eps REAL,
        bvps REAL,
        roe REAL,
        debt_to_equity REAL,
        graham_number REAL,
        recommendation TEXT,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''' )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")