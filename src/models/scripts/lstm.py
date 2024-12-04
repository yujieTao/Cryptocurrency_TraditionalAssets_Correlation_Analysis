import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader

# dataset defination
class AssetDataset(Dataset):
    def __init__(self, data, seq_length):
        self.data = data
        self.seq_length = seq_length

    def __len__(self):
        return len(self.data) - self.seq_length

    def __getitem__(self, idx):
        x = self.data[idx:idx + self.seq_length]
        y = self.data[idx + self.seq_length]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

def load_and_normalize_data(file_path):
    """
    加载并归一化数据，按列独立归一化
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file {file_path} not found!")
    
    data = pd.read_csv(file_path, index_col=0)
    data.index = pd.to_datetime(data.index)  # 确保时间序列索引
    normalized_data = (data - data.min()) / (data.max() - data.min())  # 每列归一化
    return data, normalized_data.values  # 返回原始数据和归一化矩阵

# define model
class AssetRelationshipModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(AssetRelationshipModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# training
def train_model(model, train_loader, num_epochs, learning_rate):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for inputs, targets in train_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

import matplotlib.pyplot as plt
import seaborn as sns

# Plot feature heatmap
def plot_correlation_matrix_with_labels(corr_matrix, asset_labels, output_path):

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,  # Display the correlation values on the heatmap
        fmt=".2f",   # Format the correlation values
        cmap="coolwarm",
        xticklabels=asset_labels,  # Add asset names to the x-axis
        yticklabels=asset_labels   # Add asset names to the y-axis
    )
    plt.title("LSTM Correlation Matrix Heatmap")
    plt.savefig(output_path)
    plt.close()
    print(f"Correlation heatmap with labels saved to {output_path}")

# Plot correlation heatmap
def plot_correlation_matrix(corr_matrix, output_path):
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=False, cmap="coolwarm", cbar=True)
    plt.title("LSTM Correlation Matrix Heatmap")
    plt.savefig(output_path)
    plt.close()
    print(f"Correlation heatmap saved to {output_path}")

# Modified training function to record loss
def train_model_with_loss_curve(model, train_loader, num_epochs, learning_rate):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    loss_history = []

    for epoch in range(num_epochs):
        epoch_loss = 0
        for inputs, targets in train_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        average_loss = epoch_loss / len(train_loader)
        loss_history.append(average_loss)
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {average_loss:.4f}")

    return loss_history

# Plot training loss curve
def plot_loss_curve(loss_history, output_path):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(loss_history) + 1), loss_history, marker='o')
    plt.title("Training Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    print(f"Training loss curve saved to {output_path}")

def plot_prices_and_features(prices, features, asset_labels, output_path):
    """
    Plot historical prices and extracted features for two assets.

    Args:
    - prices: DataFrame with historical prices for the assets.
    - features: NumPy array of extracted features from the LSTM model.
    - asset_labels: List of asset names.
    - output_path: File path to save the plot.
    """
    if len(asset_labels) != 2:
        raise ValueError("Please provide exactly two asset labels for comparison.")
    
    # Extract price and feature data for the two assets
    asset_1, asset_2 = asset_labels
    price_1 = prices[asset_1]
    price_2 = prices[asset_2]
    feature_1 = features[:, 0]  # First column corresponds to the first asset
    feature_2 = features[:, 1]  # Second column corresponds to the second asset
    
    # Plot the data
    plt.figure(figsize=(12, 8))
    
    # Price trends
    plt.subplot(2, 1, 1)
    plt.plot(price_1.index, price_1, label=f"{asset_1} Price", color="blue")
    plt.plot(price_2.index, price_2, label=f"{asset_2} Price", color="orange")
    plt.title("Historical Prices")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    
    # Feature trends
    plt.subplot(2, 1, 2)
    plt.plot(feature_1, label=f"{asset_1} Feature", color="green")
    plt.plot(feature_2, label=f"{asset_2} Feature", color="red")
    plt.title("Extracted Features")
    plt.xlabel("Time")
    plt.ylabel("Feature Value")
    plt.legend()
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Price and feature comparison plot saved to {output_path}")



if __name__ == "__main__":
    input_file = "/app/processed_data/processed_data.csv"
    output_features = "/app/results/lstm_features.csv"
    output_corr = "/app/results/lstm_correlation.csv"
    feature_heatmap_path = "/app/results/lstm_feature_heatmap.png"
    corr_heatmap_path = "/app/results/lstm_correlation_heatmap.png"
    labeled_corr_heatmap_path = "/app/results/lstm_correlation_heatmap_with_labels.png"
    loss_curve_path = "/app/results/lstm_loss_curve.png"

    prices = pd.read_csv(input_file, index_col=0)
    prices.index = pd.to_datetime(prices.index)  # Ensure proper datetime index


    # Check input file existence
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} not found!")

    # Load and normalize data
    data = pd.read_csv(input_file, index_col=0)
    normalized_data = (data - data.min()) / (data.max() - data.min())  # Normalize
    normalized_data = normalized_data.values

    seq_length = 10
    input_size = normalized_data.shape[1]
    hidden_size = 64
    num_layers = 2
    output_size = input_size
    batch_size = 32
    num_epochs = 10
    learning_rate = 0.001

    # Prepare dataset and dataloader
    dataset = AssetDataset(normalized_data, seq_length)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Initialize and train the model
    model = AssetRelationshipModel(input_size, hidden_size, num_layers, output_size)
    loss_history = train_model_with_loss_curve(model, train_loader, num_epochs, learning_rate)

    # Save and plot the loss curve
    plot_loss_curve(loss_history, loss_curve_path)

    # Generate features
    features = []
    with torch.no_grad():
        for i in range(len(dataset)):
            inputs, _ = dataset[i]
            inputs = inputs.unsqueeze(0)
            feature = model(inputs).squeeze().numpy()
            features.append(feature)
    features = np.array(features)

    pd.DataFrame(features).to_csv(output_features, index=False)

    # Compute and plot correlation matrix
    corr_matrix = np.corrcoef(features.T)
    pd.DataFrame(corr_matrix).to_csv(output_corr, index=False)
    print(f"Correlation matrix saved to {output_corr}")
    plot_correlation_matrix(corr_matrix, corr_heatmap_path)

    # Plot labeled correlation heatmap
    asset_labels = list(data.columns)  # Use the original column names as asset labels
    plot_correlation_matrix_with_labels(corr_matrix, asset_labels, labeled_corr_heatmap_path)


