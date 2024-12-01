import yfinance as yf
import pandas as pd

def fetch_traditional_assets(tickers, start, end):
    try:
        data = yf.download(tickers, start=start, end=end)['Adj Close']
        print("Traditional assets fetched successfully.")
        return data
    except Exception as e:
        print(f"Error fetching traditional assets: {e}")
        return pd.DataFrame()
