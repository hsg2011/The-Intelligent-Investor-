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