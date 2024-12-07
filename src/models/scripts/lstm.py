import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import seaborn as sns

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
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file {file_path} not found!")
    
    data = pd.read_csv(file_path, index_col=0)
    data.index = pd.to_datetime(data.index) 
    normalized_data = (data - data.min()) / (data.max() - data.min())
    return data, normalized_data.values

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

if __name__ == "__main__":
    output_dir = "/app/results"
    input_file = "/app/processed_data/processed_data.csv"
    output_corr = f"{output_dir}/lstm_correlation.csv"
    labeled_corr_heatmap_path = f"{output_dir}/lstm_correlation_heatmap_with_labels.png"
    loss_curve_path = f"{output_dir}/lstm_loss_curve.png"

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

    # Generate features
    features = []
    with torch.no_grad():
        for i in range(len(dataset)):
            inputs, _ = dataset[i]
            inputs = inputs.unsqueeze(0)
            feature = model(inputs).squeeze().numpy()
            features.append(feature)
    features = np.array(features)

    # Compute and plot correlation matrix
    corr_matrix = np.corrcoef(features.T)

    # Plot labeled correlation heatmap
    asset_labels = list(data.columns)  # Use the original column names as asset labels
    plot_correlation_matrix_with_labels(corr_matrix, asset_labels, labeled_corr_heatmap_path)


