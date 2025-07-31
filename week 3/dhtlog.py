import os
print("Saving CSV file to:", os.getcwd())
import serial
import csv
from datetime import datetime

# Change this to your Arduino serial port (check your IDE's port)
SERIAL_PORT = '/dev/cu.usbmodem11101'  # Example for Linux/macOS; on Windows, it might be 'COM3'
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
except Exception as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    exit(1)

try:
    with open('dht22_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write CSV header only if file is empty
        csvfile.seek(0, 2)  # Move to file end
        if csvfile.tell() == 0:
            writer.writerow(['timestamp', 'temperature', 'humidity'])

        print("Starting data logging from Arduino Serial. Press Ctrl+C to stop.")
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            # Expected format: Temp: 24.30 °C | Humidity: 43.30 %
            if line.startswith("Temp:"):
                parts = line.split('|')
                temp = parts[0].split(':')[1].strip().split(' ')[0]
                hum = parts[1].split(':')[1].strip().split(' ')[0]
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([timestamp, temp, hum])
                csvfile.flush()
                print(f"{timestamp} | Temp: {temp} °C | Humidity: {hum} %")
except KeyboardInterrupt:
    print("\nLogging stopped by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    ser.close()
