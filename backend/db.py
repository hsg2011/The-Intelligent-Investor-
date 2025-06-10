import sqlite3
from contextlib import contextmanager

DB_PATH = 'stocks.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def get_latest_stock_record(symbol: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT symbol, price, pe_ratio, market_cap,
                   eps, bvps, roe, debt_to_equity,
                   graham_number, recommendation, last_updated
            FROM stocks
            WHERE symbol = ?
            ORDER BY last_updated DESC
            LIMIT 1
        """, (symbol.upper(),))
        row = cur.fetchone()
        return dict(row) if row else None
