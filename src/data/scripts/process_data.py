import os
from datetime import datetime, timedelta
from fetch_traditional_assets import fetch_traditional_assets
from fetch_crypto_data import fetch_crypto_data

def process_data(output_dir="processed_data"):
    """
    """
    # for last three years data 
    start_date = datetime.today() - timedelta(days=1095)
    end_date = datetime.today()

    traditional_tickers = ['SPY', 'AGG', 'GLD']
    traditional_data = fetch_traditional_assets(traditional_tickers, start_date, end_date)

    crypto_symbol = 'BTC/USDT'
    crypto_data = fetch_crypto_data(crypto_symbol, start_date, end_date)

    if not traditional_data.empty and not crypto_data.empty:
        combined_data = traditional_data.join(crypto_data.rename('BTC'), how='inner').dropna()
        os.makedirs(output_dir, exist_ok=True)
        
        #store in csv file
        output_file = os.path.join(output_dir, "processed_data.csv")
        combined_data.to_csv(output_file)
        print(f"Data processing completed successfully. Data saved to {output_file}")
    else:
        print("Failed to process data: insufficient data available.")

if __name__ == "__main__":
    process_data()
