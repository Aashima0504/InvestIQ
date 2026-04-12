import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical stock data for the given ticker.
    period can be '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'.
    """
    logger.info(f"Fetching {period} historical data for {ticker}")
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    
    if hist.empty:
        raise ValueError(f"No historical data found for ticker {ticker}.")
        
    return hist

def fetch_fundamentals(ticker: str) -> dict:
    """
    Fetch fundamental data like P/E, EPS, Market Cap.
    """
    logger.info(f"Fetching fundamentals for {ticker}")
    stock = yf.Ticker(ticker)
    info = stock.info
    
    fundamentals = {
        "P/E Ratio": info.get("trailingPE", None),
        "Forward P/E": info.get("forwardPE", None),
        "EPS": info.get("trailingEps", None),
        "Market Cap": info.get("marketCap", None),
        "52 Week High": info.get("fiftyTwoWeekHigh", None),
        "52 Week Low": info.get("fiftyTwoWeekLow", None),
        "Dividend Yield": info.get("dividendYield", None),
        "Sector": info.get("sector", "Unknown"),
        "Industry": info.get("industry", "Unknown"),
    }
    return fundamentals
