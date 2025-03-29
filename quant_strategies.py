import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_historical_data(symbol, period="1y"):
    """
    Fetch historical data for the given symbol and period.
    """
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return hist

def calculate_moving_averages(df, short_window=50, long_window=200):
    """
    Calculate short-term and long-term simple moving averages (SMA).
    """
    df["SMA_short"] = df["Close"].rolling(window=short_window, min_periods=1).mean()
    df["SMA_long"] = df["Close"].rolling(window=long_window, min_periods=1).mean()
    return df

def moving_average_strategy(df):
    """
    Generate trading signals based on a moving average crossover strategy:
      - Buy signal when the short-term SMA crosses above the long-term SMA.
      - Sell signal when the short-term SMA crosses below the long-term SMA.
    
    Returns a DataFrame with signals and positions.
    """
    signals = pd.DataFrame(index=df.index)
    signals["signal"] = 0.0

    # Create the signal: 1 if short SMA > long SMA, 0 otherwise.
    signals["signal"] = (df["SMA_short"] > df["SMA_long"]).astype(int)
    
    # Generate trading orders by calculating the difference between consecutive signals.
    signals["positions"] = signals["signal"].diff()
    return signals

def plot_moving_averages(symbol, df):
    """
    Plot the stock's closing price along with its short-term and long-term moving averages.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close Price", color="blue")
    plt.plot(df.index, df["SMA_short"], label="50-Day SMA", color="red")
    plt.plot(df.index, df["SMA_long"], label="200-Day SMA", color="green")
    plt.title(f"{symbol} Stock Price and Moving Averages Over the Last Year")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_strategy(symbol, df, signals):
    """
    Plot the moving average crossover strategy.
    Buy signals (positions = 1) and sell signals (positions = -1) are marked on the plot.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close Price", color="blue")
    plt.plot(df.index, df["SMA_short"], label="50-Day SMA", color="red")
    plt.plot(df.index, df["SMA_long"], label="200-Day SMA", color="green")
    
    # Mark buy signals (short SMA crossing above long SMA)
    buy_signals = signals[signals["positions"] == 1.0]
    plt.plot(buy_signals.index, df.loc[buy_signals.index, "Close"], "^", markersize=10, color="g", label="Buy Signal")
    
    # Mark sell signals (short SMA crossing below long SMA)
    sell_signals = signals[signals["positions"] == -1.0]
    plt.plot(sell_signals.index, df.loc[sell_signals.index, "Close"], "v", markersize=10, color="r", label="Sell Signal")
    
    plt.title(f"{symbol} Moving Average Crossover Strategy")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    symbol = "AAPL"  # Change to any ticker you'd like to analyze.
    
    # Fetch one year of historical data
    df = fetch_historical_data(symbol, period="1y")
    
    # Calculate moving averages
    df = calculate_moving_averages(df, short_window=50, long_window=200)
    
    # Plot the moving averages with stock price
    plot_moving_averages(symbol, df)
    
    # Generate trading signals based on moving average crossover
    signals = moving_average_strategy(df)
    
    # Plot the trading signals
    plot_strategy(symbol, df, signals)
