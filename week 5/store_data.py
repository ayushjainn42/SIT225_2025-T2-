import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import os

# Firebase setup
databaseURL = 'https://data-capture-7a025-default-rtdb.firebaseio.com'
cred_obj = credentials.Certificate(
    '/Users/ayushjain/Desktop/SIT225 DATA CAPTURE CODES/week 5/data-capture-7a025-firebase-adminsdk-fbsvc-0c792c434d.json'
)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred_obj, {
        'databaseURL': databaseURL
    })

# Fetch data from Firebase
ref = db.reference('/gyro_data')
data = ref.get()

# Convert JSON dict to list of records
records = []
for key, val in data.items():
    records.append(val)

# Create DataFrame
df = pd.DataFrame(records)

# Clean DataFrame
df['x'] = pd.to_numeric(df['x'], errors='coerce')
df['y'] = pd.to_numeric(df['y'], errors='coerce')
df['z'] = pd.to_numeric(df['z'], errors='coerce')
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df.dropna(inplace=True)

# Save CSV in current directory
csv_path = os.path.join(os.getcwd(), 'gyro_data.csv')
df.to_csv(csv_path, index=False)
print(f"CSV saved at: {csv_path}")

import os

if os.path.exists(csv_path):
    print("✅ CSV file exists!")
else:
    print("❌ CSV file NOT found!")

print("Current working directory is:", os.getcwd())
print("Listing files in current directory:")
print(os.listdir(os.getcwd()))
