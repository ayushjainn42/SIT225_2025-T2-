import serial
import time
import random
from datetime import datetime

ser = serial.Serial('/dev/cu.usbmodem113201', 9600)
time.sleep(2)  

while True:
    num = random.randint(1, 5)
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] Sending number to Arduino: {num}")
    ser.write(f"{num}\n".encode())

    while ser.in_waiting == 0:
        pass

    received = ser.readline().decode().strip()
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] Received from Arduino: {received}")
    try:
        wait_time = int(received)
        print(f"Sleeping for {wait_time} seconds...\n")
        time.sleep(wait_time)
    except ValueError:
        print("Invalid response from Arduino.")
