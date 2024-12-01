import pandas as pd
import numpy as np
import yfinance as yf
import ccxt
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def fetch_traditional_assets(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    return data

def fetch_crypto_data(symbol, start, end):
    exchange = ccxt.binance()
    since = exchange.parse8601(start.isoformat())
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
    df = df.set_index('date')['close']
    df = df[start.date():end.date()]
    return df

def main():
    # Define time period
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)  # Last 1 year

    # Traditional assets tickers
    traditional_tickers = ['SPY', 'AGG', 'GLD']  # S&P 500 ETF, Aggregate Bond ETF, Gold ETF

    # Fetch traditional assets data
    traditional_data = fetch_traditional_assets(traditional_tickers, start_date, end_date)
    traditional_data = traditional_data.dropna()

    # Fetch cryptocurrency data
    crypto_symbol = 'BTC/USDT'
    crypto_data = fetch_crypto_data(crypto_symbol, start_date, end_date)
    crypto_data = crypto_data.rename('BTC')

    # Combine datasets
    combined_df = traditional_data.join(crypto_data, how='inner')
    combined_df = combined_df.dropna()

    # Calculate daily returns
    returns = combined_df.pct_change().dropna()

    # Calculate correlation matrix
    corr_matrix = returns.corr()

    print("Correlation Matrix:")
    print(corr_matrix)

    # Visualize correlation
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation between Traditional Assets and Bitcoin Returns')
    plt.savefig('correlation_heatmap.png')  # Save the figure
    plt.close()

if __name__ == "__main__":
    main()
