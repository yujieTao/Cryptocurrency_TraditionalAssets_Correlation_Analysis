import pandas as pd
import yfinance as yf

def fetch_crypto_data_yahoo(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data['Adj Close']
    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")
        return pd.Series()
