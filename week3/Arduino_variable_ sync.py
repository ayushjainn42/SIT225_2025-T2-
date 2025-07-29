import sys
import traceback
import os
from arduino_iot_cloud import ArduinoCloudClient
from datetime import datetime

DEVICE_ID = "3ace8a66-0f57-4cf7-b3f5-f68885409815"
SECRET_KEY = "JYEGGLedg1V4Df96tGX?m?sQ1"

LOG_FILE = "temperature_log.csv"

print("Current working directory:", os.getcwd())

def on_temperature_changed(client, value):
    timestamp = datetime.now().isoformat()
    print(f"New temperature: {value}")

    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp},{value}\n")
            f.flush()
        print(f"Logged data to {LOG_FILE}")
    except Exception as e:
        print(f"Failed to write to file: {e}")

def main():
    print("Starting Arduino Cloud Client...")

    client = ArduinoCloudClient(
        device_id=DEVICE_ID,
        username=DEVICE_ID,
        password=SECRET_KEY
    )

    client.register("temp", value=None, on_write=on_temperature_changed)

    client.start()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Error during execution")
        traceback.print_exc()
