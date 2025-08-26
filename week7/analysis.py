import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1. Read CSV data
df = pd.read_csv("/Users/ayushjain/Desktop/SIT225 DATA CAPTURE CODES/week 7/dht22_data.csv")

print(df.head())

# Function to train Linear Regression and plot
def train_and_plot(data, graph_name):
    X = data[['temperature']]  # Independent variable
    y = data['humidity']       # Dependent variable

    # 2. Train Linear Regression
    model = LinearRegression()
    model.fit(X, y)

    # 3. Generate 100 test temperature points
    min_temp = data['temperature'].min()
    max_temp = data['temperature'].max()
    test_temps = np.linspace(min_temp, max_temp, 100).reshape(-1, 1)

    # Predict humidity for test temperatures
    predicted_humidity = model.predict(test_temps)

    # 4. Plot scatter + trend line
    plt.figure(figsize=(8,5))
    plt.scatter(data['temperature'], data['humidity'], label='Original Data')
    plt.plot(test_temps, predicted_humidity, color='red', label='Trend Line')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.title(f'Temperature vs Humidity - {graph_name}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{graph_name}.png")
    plt.show()

    return model, test_temps, predicted_humidity

# --- Step A: Original data ---
model_raw, test_temps_raw, predicted_raw = train_and_plot(df, "graph_raw")

# --- Step B: Filter some outliers ---
# Example: Remove top 5% highest temperatures and lowest 5% lowest temperatures
lower_bound = df['temperature'].quantile(0.05)
upper_bound = df['temperature'].quantile(0.95)
df_filtered1 = df[(df['temperature'] >= lower_bound) & (df['temperature'] <= upper_bound)]

model_filtered1, test_temps_f1, predicted_f1 = train_and_plot(df_filtered1, "graph_filtered1")

# --- Step C: Further filter more extreme outliers ---
lower_bound2 = df['temperature'].quantile(0.10)
upper_bound2 = df['temperature'].quantile(0.90)
df_filtered2 = df[(df['temperature'] >= lower_bound2) & (df['temperature'] <= upper_bound2)]

model_filtered2, test_temps_f2, predicted_f2 = train_and_plot(df_filtered2, "graph_filtered2")

print("All graphs saved: graph_raw.png, graph_filtered1.png, graph_filtered2.png")
print("You can insert these graphs into your PDF for submission.")
