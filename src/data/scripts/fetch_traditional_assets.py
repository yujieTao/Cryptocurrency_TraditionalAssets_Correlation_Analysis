import yfinance as yf
import pandas as pd

def fetch_traditional_assets(tickers, start, end):
    try:
        data = yf.download(tickers, start=start, end=end)['Adj Close']
        print(f"Fetched traditional assets data range: {data.index.min()} to {data.index.max()}")
        return data
    except Exception as e:
        print(f"Failed download: {tickers}: {e}")
        return pd.DataFrame()
