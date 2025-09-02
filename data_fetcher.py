import yfinance as yf

def fetch_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "price": info.get("currentPrice"),
        "eps": info.get("trailingEps"),
        "growth": info.get("earningsEstimate5Y") or info.get("earningsGrowth"),
        "dividend": info.get("dividendRate"),
        "pe_ratio": info.get("trailingPE"),
        "sector_pe": 15
    }

def fetch_historical_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y")
        eps = stock.info.get("trailingEps", 1)
        hist["EPS"] = eps if eps else 1
        return hist
    except Exception as e:
        print("❌ Błąd pobierania danych historycznych:", e)
        return None
