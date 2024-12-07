import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def ensure_output_directory(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    print(f"Loaded data:\n{data.head()}")
    return data

def calculate_returns(data):
    returns = data.pct_change().dropna()
    print("Calculated daily returns:\n", returns.head())
    return returns

def analyze_correlation(returns, output_path):
    ensure_output_directory(os.path.dirname(output_path))
    corr_matrix = returns.corr(method='pearson')
    print("Correlation Matrix:\n", corr_matrix)
    corr_matrix.to_csv(output_path)
    print(f"Correlation matrix saved to {output_path}")
    return corr_matrix

def plot_correlation_heatmap(corr_matrix, title, output_path):
    ensure_output_directory(os.path.dirname(output_path))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(title)
    plt.savefig(output_path)
    plt.close()
    print(f"Correlation heatmap saved to {output_path}")

def rolling_correlation_multi(data, base_asset, compare_assets, window, output_path):
    ensure_output_directory(os.path.dirname(output_path))
    missing_assets = [asset for asset in compare_assets if asset not in data.columns]
    if missing_assets:
        print(f"Warning: The following assets are missing from the dataset: {missing_assets}")
        compare_assets = [asset for asset in compare_assets if asset in data.columns]
    if not compare_assets:
        print("No valid assets to compare. Skipping rolling correlation plot.")
        return

    plt.figure(figsize=(12, 6))
    for asset in compare_assets:
        rolling_corr = data[base_asset].rolling(window=window).corr(data[asset])
        plt.plot(rolling_corr, label=f"{base_asset} vs {asset} (Rolling {window} Days)")
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.title(f"Rolling Correlation: {base_asset} vs Multiple Assets")
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.legend()
    plt.savefig(output_path)
    plt.close()
    print(f"Rolling correlation plot saved to {output_path}")

def main(file_path, output_dir):
    ensure_output_directory(output_dir)

    data = load_data(file_path)
    returns = calculate_returns(data)

    corr_csv = os.path.join(output_dir, "correlation_matrix.csv")
    corr_matrix = analyze_correlation(returns, output_path=corr_csv)

    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    plot_correlation_heatmap(corr_matrix, title="Correlation Heatmap", output_path=heatmap_path)

    rolling_corr_path = os.path.join(output_dir, "rolling_correlation_multi.png")
    rolling_correlation_multi(returns, base_asset="BTC", compare_assets=["SPY", "GLD", "AGG"], window=30, output_path=rolling_corr_path)

    print("All analyses completed!")

if __name__ == "__main__":
    input_file = "/app/processed_data/processed_data.csv"
    output_dir = "/app/results"
    main(input_file, output_dir)
