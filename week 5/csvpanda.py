import pandas as pd

# Step 1: Load the CSV file
csv_file = "8f17d22d-92b6-4094-9c87-76cdce3e6a55.csv"
sensor_data = pd.read_csv(csv_file)

# Step 2: Show first 5 rows
print("First 5 rows of data:")
print(sensor_data.head())
print("\n")

# Step 3: Check structure of the dataset
print("Dataset info:")
print(sensor_data.info())
print("\n")

# Step 4: Check for missing values
print("Missing values per column:")
print(sensor_data.isnull().sum())
print("\n")

# Step 5: Try converting 'timestamp' column to datetime (if it exists)
if 'timestamp' in sensor_data.columns:
    sensor_data['timestamp'] = pd.to_datetime(sensor_data['timestamp'], errors='coerce')
    print("Timestamp column converted to datetime.")
    print("\n")

# Step 6: Rename columns (example: change generic names to meaningful ones)
# You can customize these based on actual column names
sensor_data.rename(columns={
    'val1': 'Temperature',
    'val2': 'Humidity'
}, inplace=True)

# Step 7: Convert numeric columns safely
for col in ['Temperature', 'Humidity']:
    if col in sensor_data.columns:
        sensor_data[col] = pd.to_numeric(sensor_data[col], errors='coerce')

# Step 8: Handle missing values (optional - choose one)
sensor_data.dropna(inplace=True)  # Remove rows with any missing values
# OR: sensor_data.fillna(method='ffill', inplace=True)  # Forward-fill missing values

# Step 9: Set timestamp as index (if time series)
if 'timestamp' in sensor_data.columns:
    sensor_data.set_index('timestamp', inplace=True)

# Final: Display cleaned data summary
print("Cleaned dataset summary:")
print(sensor_data.describe())
