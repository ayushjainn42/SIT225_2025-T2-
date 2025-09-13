# task3_separate_csvs.py
# Q3: Three CSVs (accel_x.csv, accel_y.csv, accel_z.csv), each line "<timestamp>,<value>"
from datetime import datetime
from pathlib import Path
from arduino_iot_cloud import ArduinoCloudClient
from iot_secrets import DEVICE_ID, SECRET_KEY

# If your Python Thing variable names differ, change these:
VAR_X = "accelerometer_x"
VAR_Y = "accelerometer_y"
VAR_Z = "accelerometer_z"

# Write next to this script in ./data
OUTDIR = Path(_file_).resolve().parent / "data"
OUTDIR.mkdir(parents=True, exist_ok=True)
fx = (OUTDIR / "accel_x.csv").open("a", buffering=1, encoding="utf-8", newline="")
fy = (OUTDIR / "accel_y.csv").open("a", buffering=1, encoding="utf-8", newline="")
fz = (OUTDIR / "accel_z.csv").open("a", buffering=1, encoding="utf-8", newline="")

def ts():
    return datetime.now().isoformat(timespec="seconds")

def on_x(_c, value):
    try:
        val = float(value)
    except Exception:
        return
    line = f"{ts()},{val}\n"
    fx.write(line)
    print("X:", line.strip())

def on_y(_c, value):
    try:
        val = float(value)
    except Exception:
        return
    line = f"{ts()},{val}\n"
    fy.write(line)
    print("Y:", line.strip())

def on_z(_c, value):
    try:
        val = float(value)
    except Exception:
        return
    line = f"{ts()},{val}\n"
    fz.write(line)
    print("Z:", line.strip())

def main():
    print(f"Writing to: {OUTDIR}")
    print("Keep Arduino IoT Remote open (foreground), Phone-as-device ON, Accel X/Y/Z ON.")
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register(VAR_X, value=None, on_write=on_x)
    client.register(VAR_Y, value=None, on_write=on_y)
    client.register(VAR_Z, value=None, on_write=on_z)
    client.start()  # blocks; Ctrl+C to stop

if _name_ == "_main_":
    main()