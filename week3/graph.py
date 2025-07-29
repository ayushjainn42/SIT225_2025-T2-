import matplotlib.pyplot as plt
import csv
from datetime import datetime

timestamps = []
temperatures = []

# Replace 'temperature_log.csv' with your file path if different
with open('temperature_log.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # Parse timestamp and temperature value
        timestamps.append(datetime.fromisoformat(row[0]))
        temperatures.append(float(row[1]))

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(timestamps, temperatures, marker='o', linestyle='-')
plt.title("Temperature vs Time")
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
