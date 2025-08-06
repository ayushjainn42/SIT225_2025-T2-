import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv('gyro_data.csv')

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Plot each axis separately
for axis in ['x', 'y', 'z']:
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df[axis])
    plt.title(f'Gyroscope {axis.upper()} axis over time')
    plt.xlabel('Timestamp')
    plt.ylabel('Rotation rate (deg/s)')
    plt.grid(True)
    plt.show()

# Plot all axes together
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['x'], label='X axis')
plt.plot(df['timestamp'], df['y'], label='Y axis')
plt.plot(df['timestamp'], df['z'], label='Z axis')
plt.title('Gyroscope readings over time')
plt.xlabel('Timestamp')
plt.ylabel('Rotation rate (deg/s)')
plt.legend()
plt.grid(True)
plt.show()
