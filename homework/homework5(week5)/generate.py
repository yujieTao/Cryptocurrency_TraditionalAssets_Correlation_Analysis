import pandas as pd
import numpy as np
import time
import os

# Create the directory if it doesn't exist
output_dir = "homework5"
os.makedirs(output_dir, exist_ok=True)

# Create DataFrame with 1e6 rows and 5 columns, two columns identical
rows = int(1e6)
data = {
    'col1': np.random.rand(rows),
    'col2': np.random.rand(rows),
    'col3': np.random.rand(rows),
    'col4': np.random.rand(rows),  # This will be identical to col1
    'col5': np.random.rand(rows)   # This will be identical to col2
}

df = pd.DataFrame(data)
df['col4'] = df['col1']  # Make 'col4' identical to 'col1'
df['col5'] = df['col2']  # Make 'col5' identical to 'col2'

# Initialize time records
time_records = {}

# Save the DataFrame to different formats and record the time
# HDF
start_time = time.time()
df.to_hdf(os.path.join(output_dir, 'data.h5'), key='df', mode='w')
time_records['HDF'] = time.time() - start_time

# Feather
start_time = time.time()
df.to_feather(os.path.join(output_dir, 'data.feather'))
time_records['Feather'] = time.time() - start_time

# Parquet
start_time = time.time()
df.to_parquet(os.path.join(output_dir, 'data.parquet'))
time_records['Parquet'] = time.time() - start_time

# Write times to a .txt file
with open(os.path.join(output_dir, 'times.txt'), 'w') as f:
    for format, duration in time_records.items():
        f.write(f"{format} format: {duration:.6f} seconds\n")

print("Data saved and times recorded.")
