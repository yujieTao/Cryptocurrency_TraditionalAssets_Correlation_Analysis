import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# create output path
def ensure_output_directory(output_path="output"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

# load data, Set date as index
def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    print(f"Loaded data:\n{data.head()}")
    return data

# Calculate daily return
def calculate_returns(data):
    returns = data.pct_change().dropna()
    print("Calculated daily returns:\n", returns.head())
    return returns

# correlation analysis
def analyze_correlation(returns, output_path="output/correlation_matrix.csv"):
    ensure_output_directory(os.path.dirname(output_path))
    corr_matrix = returns.corr(method='pearson')  # Pearson correlation
    print("Correlation Matrix:\n", corr_matrix)
    corr_matrix.to_csv(output_path)  # 保存为CSV
    print(f"Correlation matrix saved to {output_path}")
    return corr_matrix

# heatmap
def plot_correlation_heatmap(corr_matrix, title="Correlation Heatmap", output_path="output/correlation_heatmap.png"):
    ensure_output_directory(os.path.dirname(output_path))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(title)
    plt.savefig(output_path)  
    plt.close()
    print(f"Correlation heatmap saved to {output_path}")



# rolling correlation analysis for multiple assets
def rolling_correlation_multi(data, base_asset, compare_assets, window=30, output_path="output/rolling_correlation_multi.png"):
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




def main(file_path):
    ensure_output_directory("output")

    data = load_data(file_path)

    returns = calculate_returns(data)

    corr_matrix = analyze_correlation(returns, output_path="output/correlation_matrix.csv")

    plot_correlation_heatmap(corr_matrix, title="Correlation Heatmap", output_path="output/correlation_heatmap.png")

    # Rolling correlation for BTC vs SPY, GLD, and AGG
    rolling_correlation_multi(
        returns, 
        base_asset="BTC", 
        compare_assets=["SPY", "GLD", "AGG"], 
        window=30, 
        output_path="output/rolling_correlation_multi.png"
    )

    print("All analyses completed!")



if __name__ == "__main__":
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    csv_file_path = os.path.join(base_dir, "data", "processed_data", "processed_data.csv")
    print(f"Using relative path: {csv_file_path}")
    

    main(csv_file_path)


