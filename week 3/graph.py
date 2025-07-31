import pandas as pd
import matplotlib.pyplot as plt

# Exact path to your CSV file
file_path = "/Users/ayushjain/Desktop/SIT225 DATA CAPTURE CODES/week 3/dht22_data.csv"

# Load the data
df = pd.read_csv(file_path)

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Ensure temperature and humidity are floats
df['temperature'] = df['temperature'].astype(float)
df['humidity'] = df['humidity'].astype(float)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', color='red')
plt.plot(df['timestamp'], df['humidity'], label='Humidity (%)', color='blue')

plt.xlabel('Timestamp')
plt.ylabel('Sensor Values')
plt.title('DHT22 Sensor Readings Over Time')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
