import os
from datetime import datetime, timedelta
from fetch_traditional_assets import fetch_traditional_assets
from fetch_crypto_data import fetch_crypto_data_yahoo

def process_data(output_dir="processed_data"):
    """
    Process data for traditional assets and crypto assets, combining them into a single dataset.
    """
    # Define time range
    start_date = datetime.today() - timedelta(days=3*365)
    end_date = datetime.today()

    print(f"Fetching data from {start_date.date()} to {end_date.date()}")

    # Fetch traditional assets
    traditional_tickers = ['SPY', 'AGG', 'GLD']
    traditional_data = fetch_traditional_assets(traditional_tickers, start_date, end_date)

    # Fetch crypto data
    crypto_symbol = 'BTC-USD'  # Use Yahoo Finance format for BTC
    crypto_data = fetch_crypto_data_yahoo(crypto_symbol, start_date, end_date)
    print(f"Fetched BTC data range: {crypto_data.index.min()} to {crypto_data.index.max()}")
    if crypto_data.empty or traditional_data.empty:
        print("Failed to process data: insufficient data available.")
        return

    # Rename crypto data seriesx
    crypto_data.name = 'BTC'

    # Combine datasets
    combined_data = traditional_data.join(crypto_data, how='inner').dropna()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save combined data
    output_file = os.path.join(output_dir, "processed_data.csv")
    combined_data.to_csv(output_file)
    print(f"Data processing completed successfully. Data saved to {output_file}")

if __name__ == "__main__":
    process_data()
