import os
import pandas as pd
import numpy as np
import yfinance as yf
import ccxt
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def fetch_traditional_assets(tickers, start, end):
    try:
        data = yf.download(tickers, start=start, end=end)['Adj Close']
        return data
    except Exception as e:
        print(f"Failed download: {tickers}: {e}")
        return pd.DataFrame()

def fetch_crypto_data(symbol, start, end):
    try:
        exchange = ccxt.binance()
        since = exchange.parse8601(start.isoformat())
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', since=since)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df = df.set_index('date')['close']
        df = df[start.date():end.date()]
        return df
    except Exception as e:
        print(f"Failed to fetch crypto data for {symbol}: {e}")
        return pd.Series()

def main():
    # 定义时间范围
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)  # 过去1年

    # 传统资产标的
    traditional_tickers = ['SPY', 'AGG', 'GLD']  # S&P 500 ETF, Aggregate Bond ETF, Gold ETF

    # 获取传统资产数据
    traditional_data = fetch_traditional_assets(traditional_tickers, start_date, end_date)
    if traditional_data.empty:
        print("No traditional asset data fetched.")
    else:
        traditional_data = traditional_data.dropna()

    # 获取加密货币数据
    crypto_symbol = 'BTC/USDT'
    crypto_data = fetch_crypto_data(crypto_symbol, start_date, end_date)
    if crypto_data.empty:
        print("No crypto data fetched.")
    else:
        crypto_data = crypto_data.rename('BTC')

    # 合并数据
    combined_df = traditional_data.join(crypto_data, how='inner')
    if combined_df.empty:
        print("No combined data available.")
    else:
        combined_df = combined_df.dropna()

    # 计算每日收益率
    returns = combined_df.pct_change().dropna()

    # 计算相关性矩阵
    corr_matrix = returns.corr()

    print("Correlation Matrix:")
    print(corr_matrix)

    # 确保 output 目录存在
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 可视化相关性
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation between Traditional Assets and Bitcoin Returns')
    plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))  # 保存图片到 output 目录
    plt.close()
    print(f"Correlation heatmap saved to {os.path.join(output_dir, 'correlation_heatmap.png')}")

if __name__ == "__main__":
    main()
