from datetime import datetime
import threading
import time
import cv2
import pandas as pd
import os

from arduino_iot_cloud import ArduinoCloudClient
from iot_secrets import DEVICE_ID, SECRET_KEY
from smoothdash import make_smooth_app
from dash import html


VAR_X = "accelerometer_x"
VAR_Y = "accelerometer_y"
VAR_Z = "accelerometer_z"

WINDOW_POINTS = 200
MAX_APPEND    = 15
POLL_MS       = 150
SAVE_INTERVAL = 1     # seconds between saves
SAVE_DIR      = "data"

os.makedirs(SAVE_DIR, exist_ok=True)

# Single CSV log file
csv_file = os.path.join(SAVE_DIR, "accelerometer_log.csv")
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["time","x","y","z","image"]).to_csv(csv_file, index=False)


app, state = make_smooth_app(
    ["X", "Y", "Z"],
    window_points=WINDOW_POINTS,
    max_append=MAX_APPEND,
    poll_ms=POLL_MS,
)
push = state["push"]

app.layout.children.append(html.Div("📡 Auto-saving to single CSV every 10s...", id="info"))


latest = {"x": None, "y": None, "z": None}
seen   = {"x": False, "y": False, "z": False}
lock = threading.Lock()

# Buffer for last 10s of samples
buffer = []

seq_num = 1  # sequence number for images

def _try_emit():
    """Emit new accelerometer sample and store in buffer."""
    if seen["x"] and seen["y"] and seen["z"]:
        ts = datetime.now().strftime("%H:%M:%S")   # proper timestamp
        row = (ts, latest["x"], latest["y"], latest["z"])
        buffer.append(row)
        push(ts, latest["x"], latest["y"], latest["z"])
        seen["x"] = seen["y"] = seen["z"] = False

def on_x(_client, v):
    with lock:
        latest["x"] = float(v) if v is not None else None
        seen["x"] = True
        _try_emit()

def on_y(_client, v):
    with lock:
        latest["y"] = float(v) if v is not None else None
        seen["y"] = True
        _try_emit()

def on_z(_client, v):
    with lock:
        latest["z"] = float(v) if v is not None else None
        seen["z"] = True
        _try_emit()

# Webcam capture

def capture_webcam_image(filename):
    cam = cv2.VideoCapture(1)  # laptop camera index
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(filename, frame)
    cam.release()


def autosave_loop():
    global seq_num, buffer
    while True:
        time.sleep(SAVE_INTERVAL)
        if not buffer:
            continue

        # Capture image for this 10s window
        ts_file = datetime.now().strftime("%H%M")
        img_filename = f"{seq_num}_{ts_file}.jpg"
        img_path = os.path.join(SAVE_DIR, img_filename)
        capture_webcam_image(img_path)

 
        df = pd.DataFrame(buffer, columns=["time","x","y","z"])
        df["image"] = img_path
        df.to_csv(csv_file, mode="a", header=False, index=False)

        print(f"[UPDATED] {csv_file} with {len(buffer)} rows, image: {img_path}")

        buffer = []  # clear buffer for next window
        seq_num += 1


# Cloud thread
def start_cloud_thread():
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register(VAR_X, value=None, on_write=on_x)
    client.register(VAR_Y, value=None, on_write=on_y)
    client.register(VAR_Z, value=None, on_write=on_z)

    def run():
        print("[Cloud] Connecting... keep the phone app in the foreground.")
        client.start()

    th = threading.Thread(target=run, daemon=True)
    th.start()
    return th


if __name__ == "__main__":
    start_cloud_thread()
    threading.Thread(target=autosave_loop, daemon=True).start()
    print("Dash running at http://127.0.0.1:8050")
    app.run(debug=False, host="127.0.0.1", port=8050)
