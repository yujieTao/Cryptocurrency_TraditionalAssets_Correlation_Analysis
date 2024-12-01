import ccxt
import pandas as pd

def fetch_crypto_data(symbol, start, end):
    try:
        exchange = ccxt.binance()
        since = exchange.parse8601(start.isoformat())
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', since=since)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df = df.set_index('date')['close']
        df = df[start.date():end.date()]
        print("Crypto data fetched successfully.")
        return df
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return pd.Series()
