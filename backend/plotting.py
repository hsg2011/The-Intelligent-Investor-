import io
import matplotlib.pyplot as plt
import yfinance as yf
from fastapi.responses import StreamingResponse

plt.switch_backend('Agg')  # For headless environments

def plot_price(symbol: str):
    df = yf.Ticker(symbol).history(period='1y')
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'], label='Close')
    ax.set_title(f"{symbol} Price (1Y)")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')

def plot_pe(symbol: str):
    # Assume historical P/E stored in DB; for example purposes, fetch daily forwardPE
    df = yf.Ticker(symbol).history(period='1y')
    # P/E not in history; skip or plot flat placeholder
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'] / df['Close'], label='P/E placeholder')
    ax.set_title(f"{symbol} P/E (1Y)")
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')