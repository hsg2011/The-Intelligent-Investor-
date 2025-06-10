import math

def analyze_stock_combined(symbol, price, pe_ratio, market_cap, eps, bvps, roe, debt_to_equity):
    # Validate inputs
    if None in (price, eps, bvps, roe, debt_to_equity):
        return "No Data Available"

    # Convert to float
    price = float(price)
    eps = float(eps)
    bvps = float(bvps)
    roe = float(roe)
    debt_to_equity = float(debt_to_equity)

    # Graham Number calculation
    graham_number = math.sqrt(22.5 * eps * bvps)

    # Graham recommendation
    if price < graham_number:
        graham_rec = f"BUY (Graham {graham_number:.2f})"
    elif price > graham_number:
        graham_rec = f"SELL (Graham {graham_number:.2f})"
    else:
        graham_rec = f"HOLD (Graham {graham_number:.2f})"

    # Buffett criteria
    if roe >= 0.15 and debt_to_equity < 0.5 and price < graham_number:
        buffett_rec = "BUFFETT PICK"
    else:
        buffett_rec = ""

    return f"{graham_rec}" + (f" | {buffett_rec}" if buffett_rec else "")