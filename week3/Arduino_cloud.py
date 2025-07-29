import traceback
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "2e170cae-dd27-48f9-b92c-8e43d51988d6"
SECRET_KEY = "3Rmc7zIz99a!WaiSQxG@cP8uii"
USERNAME = "s225476349@deakin.edu.au"  # Your Arduino Cloud account email


def on_temperature_changed(client, value):
    print(f"New temperature: {value}")

def main():
    print("Starting Arduino Cloud client...")
    print(f"Device ID: {DEVICE_ID}")
    print(f"Username: {USERNAME}")
    print(f"Secret Key: {SECRET_KEY[:4]}... (hidden)")

    client = ArduinoCloudClient(
        device_id=DEVICE_ID,
        username=USERNAME,
        password=SECRET_KEY
    )

    client.register(
        "temperature",
        value=None,
        on_write=on_temperature_changed
    )

    client.start()  # This runs the internal loop and listens for updates

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
