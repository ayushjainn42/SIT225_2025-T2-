import serial
import datetime
import firebase_admin
from firebase_admin import credentials, db
import os

print("Current working directory:", os.getcwd())
csv_path = os.path.join(os.getcwd(), 'gyro_data.csv')
print("CSV file path will be:", csv_path)

df.to_csv(csv_path, index=False)
print("CSV saved successfully!")

# Firebase setup
databaseURL = 'https://data-capture-7a025-default-rtdb.firebaseio.com'
cred_obj = credentials.Certificate(
    '/Users/ayushjain/Desktop/SIT225 DATA CAPTURE CODES/week 5/data-capture-7a025-firebase-adminsdk-fbsvc-0c792c434d.json'
)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})


ser = serial.Serial('/dev/cu.usbmodem113201', 9600)


try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                x, y, z = map(float, line.split(','))
                timestamp = datetime.datetime.now().isoformat()

                data = {
                    "timestamp": timestamp,
                    "x": x,
                    "y": y,
                    "z": z
                }

                ref = db.reference('/gyro_data')
                ref.push(data)

                print("Uploaded:", data)

            except ValueError:
                print("Invalid data:", line)
except KeyboardInterrupt:
    print("Stopped by user.")
