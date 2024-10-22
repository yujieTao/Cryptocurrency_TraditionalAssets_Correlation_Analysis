import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'data/coding-environment-exercise.csv'
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['date'], data['value'], marker='o', linestyle='-', color='b')

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Time Series of Values from CSV')
plt.grid(True)

# Save the plot as a PNG file
output_path = 'output/plot.png'
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_path)

# Print confirmation
print(f"Plot saved to {output_path}")
