from datetime import datetime
import threading

from arduino_iot_cloud import ArduinoCloudClient
from iot_secrets import DEVICE_ID, SECRET_KEY
from smoothdash import make_smooth_app


VAR_X = "accelerometer_x"
VAR_Y = "accelerometer_y"
VAR_Z = "accelerometer_z"


WINDOW_POINTS = 600   
MAX_APPEND    = 15   
POLL_MS       = 150  


app, state = make_smooth_app(
    ["X", "Y", "Z"],
    window_points=WINDOW_POINTS,
    max_append=MAX_APPEND,
    poll_ms=POLL_MS,
)
push = state["push"]


latest = {"x": None, "y": None, "z": None}
seen   = {"x": False, "y": False, "z": False}
lock = threading.Lock()

def _try_emit():

    if seen["x"] and seen["y"] and seen["z"]:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
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
    print("Dash at http://127.0.0.1:8050")
    app.run(debug=False, host="127.0.0.1", port=8050) 
