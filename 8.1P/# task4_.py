# task4_.py
# Q4: One combined CSV (accel_xyz.csv), each line "<timestamp>,<x>,<y>,<z>"
# Minimal, cloud-probe style: define callbacks, write + print a row when all 3 axes have updated.

from datetime import datetime
from pathlib import Path
from arduino_iot_cloud import ArduinoCloudClient
from secret import DEVICE_ID, SECRET_KEY

# Use your Arduino Cloud variable names:
VAR_X = "accelerometer_x"
VAR_Y = "accelerometer_y"
VAR_Z = "accelerometer_z"

# Write next to this script in ./data
OUTDIR = Path(__file__).resolve().parent / "data"
OUTDIR.mkdir(parents=True, exist_ok=True)
csv_path = OUTDIR / "accel_xyz.csv"

# Add a header the first time
new_file = (not csv_path.exists()) or csv_path.stat().st_size == 0
f = csv_path.open("a", buffering=1, encoding="utf-8", newline="")
if new_file:
    f.write("timestamp,x,y,z\n")

# Keep latest values + flags so we only write when we have a fresh trio
latest = {"x": None, "y": None, "z": None}
seen   = {"x": False, "y": False, "z": False}

def ts():
    return datetime.now().isoformat(timespec="seconds")

def coerce_float(v):
    try:
        return float(v)
    except Exception:
        pass
    # Be tolerant if library/object wraps the number
    try:
        return float(getattr(v, "value"))
    except Exception:
        pass
    if isinstance(v, dict):
        for k in ("value", "last_value", "v", "val"):
            if k in v:
                try:
                    return float(v[k])
                except Exception:
                    pass
    return None

def maybe_write_row():
    if seen["x"] and seen["y"] and seen["z"]:
        line = f"{ts()},{latest['x']},{latest['y']},{latest['z']}\n"
        f.write(line)
        print("Accel values:", line.strip())  # console feedback like cloud_probe
        seen["x"] = seen["y"] = seen["z"] = False  # reset for next trio

def on_x(_c, value):
    val = coerce_float(value)
    if val is None:
        return
    latest["x"] = val
    seen["x"] = True
    maybe_write_row()

def on_y(_c, value):
    val = coerce_float(value)
    if val is None:
        return
    latest["y"] = val
    seen["y"] = True
    maybe_write_row()

def on_z(_c, value):
    val = coerce_float(value)
    if val is None:
        return
    latest["z"] = val
    seen["z"] = True
    maybe_write_row()

def main():
    print(f"Writing combined CSV to: {csv_path}")
    print("Keep Arduino IoT Remote OPEN (foreground), Phone-as-device ON, Accel X/Y/Z ON.")
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register(VAR_X, value=None, on_write=on_x)
    client.register(VAR_Y, value=None, on_write=on_y)
    client.register(VAR_Z, value=None, on_write=on_z)
    try:
        client.start()  # blocks; Ctrl+C to stop
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        try:
            f.close()
        except:
            pass

if __name__ == "__main__":
    main()