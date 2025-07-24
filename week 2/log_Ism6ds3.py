import serial
import time


port = '/dev/cu.usbmodem11401' 
baud = 9600

filename = "log_data.csv"

# Open serial connection and file
ser = serial.Serial(port, baud)
time.sleep(2)  # wait for Arduino to reboot

with open(filename, 'w') as file:
    file.write("Timestamp, X, Y, Z\n")
    print("Logging started... Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line and "X, Y, Z" not in line:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{timestamp}, {line}\n")
                print(f"{timestamp}, {line}")
    except KeyboardInterrupt:
        print("Logging stopped.")
        ser.close()
