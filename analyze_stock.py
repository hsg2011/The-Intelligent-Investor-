#Analyze PE ration

import math

import math

def analyze_stock(symbol, stock_price, pe_ratio, market_cap, eps, bvps):
    # Ensure all required values are present
    if pe_ratio is None or stock_price is None or eps is None or bvps is None:
        return "No Data Available"

    try:
        # Convert to float to be safe
        pe_ratio = float(pe_ratio)
        stock_price = float(stock_price)
        eps = float(eps)
        bvps = float(bvps)
    except Exception as e:
        return "Data Conversion Error"

    # Calculate Graham Number: sqrt(22.5 * EPS * BVPS)
    graham_number = math.sqrt(22.5 * eps * bvps)

    # Debug print (optional)
    print(f"DEBUG - {symbol}: EPS = {eps}, BVPS = {bvps}, Graham Number = {graham_number:.2f}, Stock Price = {stock_price}")

    # Determine recommendation based on the Graham Number
    if stock_price < graham_number:
        return f"BUY (Undervalued, Graham Number = {graham_number:.2f})"
    elif stock_price > graham_number:
        return f"SELL (Overvalued, Graham Number = {graham_number:.2f})"
    else:
        return f"HOLD (Fairly Priced, Graham Number = {graham_number:.2f})"
