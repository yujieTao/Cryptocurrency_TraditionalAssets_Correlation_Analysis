import yfinance as yf
import ccxt


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
