#Analyze PE ration

def analyze_stock1(symbol,stock_price,pe_ratio,  market_cp):
    pe_ratio = float(pe_ratio)

    print(pe_ratio)
    if pe_ratio is None or stock_price is None:
        return "No Data"
    
    if pe_ratio < 15.00:
        return "BUY"
    elif pe_ratio >25.00:
        return "SELL"
    else:
        return "HOLD"