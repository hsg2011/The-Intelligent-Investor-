import pandas as pd
import sqlite3
from db import get_db_connection

WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

def update_sp500_symbols():
    table = pd.read_html(WIKI_URL)[0]
    symbols = table['Symbol'].tolist()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        for sym in symbols:
            cursor.execute(
                "INSERT OR IGNORE INTO sp500_symbols(symbol) VALUES (?)", (sym,)
            )
        conn.commit()

def get_sp500_symbols():
    with get_db_connection() as conn:
        rows = conn.execute("SELECT symbol FROM sp500_symbols").fetchall()
    return [r[0] for r in rows]