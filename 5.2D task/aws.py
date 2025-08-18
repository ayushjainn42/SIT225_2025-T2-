import paho.mqtt.client as mqtt
import json, time
from pymongo import MongoClient
import boto3
import pandas as pd
import matplotlib.pyplot as plt
import threading

# -----------------------------
# MongoDB setup (DB-1)
# -----------------------------
mongo_client = MongoClient(
    "mongodb+srv://meinhoonayush:Mona%401973@cluster0.jmahznh.mongodb.net/?retryWrites=true&w=majority"
)
db1 = mongo_client["GyroDB"]
collection1 = db1["gyro_data"]

# -----------------------------
# DynamoDB setup (DB-2)
# -----------------------------
aws_region = 'ap-southeast-2'  # Your region
aws_access_key_id = "AKIASNMSFWZEIWYTAXPG"
aws_secret_access_key = "wrOG/l01tP4BqdJcy3HwVmsRlbuF5Js/PMpjvBc2"

dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

table_name = "GyroData"

# Check if table exists, else create
existing_tables = [table.name for table in dynamodb.tables.all()]
if table_name not in existing_tables:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],  # Partition key
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    print(f"Creating DynamoDB table '{table_name}'...")
    table.wait_until_exists()
    print("Table created successfully!")
else:
    table = dynamodb.Table(table_name)

# -----------------------------
# HiveMQ MQTT setup
# -----------------------------
broker = "f5e7e9613317481bbc8ad4efc9918939.s1.eu.hivemq.cloud"
port = 8883
topic = "nano33/gyroscope"
username = "meinhoonayush"
password = "Mona@1973"

# -----------------------------
# Callback for incoming MQTT messages
# -----------------------------
data_list = []

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload["timestamp"] = time.time()
        print("Received:", payload)

        # Store to MongoDB
        collection1.insert_one(payload)

        # Store to DynamoDB
        table.put_item(Item={
            "id": str(int(payload["timestamp"])),
            "x": str(payload["x"]),
            "y": str(payload["y"]),
            "z": str(payload["z"])
        })

        # Append to local list for CSV/plot
        data_list.append(payload)
    except Exception as e:
        print("Error:", e)

# -----------------------------
# MQTT client setup
# -----------------------------
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()  # SSL/TLS
client.on_message = on_message

print("Connecting to MQTT broker...")
client.connect(broker, port, 60)
client.subscribe(topic)
print("Subscribed to topic:", topic)

# Run MQTT client in background thread
def run_mqtt():
    client.loop_forever()

thread = threading.Thread(target=run_mqtt)
thread.start()

# -----------------------------
# Data collection duration
# -----------------------------
collect_seconds = 30  # Change to longer if needed
print(f"Collecting data for {collect_seconds} seconds...")
time.sleep(collect_seconds)

# Stop MQTT loop
client.disconnect()
thread.join()
print("Data collection complete!")

# -----------------------------
# Save data to CSV
# -----------------------------
df = pd.DataFrame(data_list)
df.to_csv("gyro_data.csv", index=False)
print("CSV saved as gyro_data.csv")

# -----------------------------
# Plot graphs
# -----------------------------
plt.figure(figsize=(12, 8))

# Individual x, y, z plots
plt.subplot(3, 1, 1)
plt.plot(df['timestamp'], df['x'], color='r')
plt.title('Gyroscope X')
plt.xlabel('Timestamp')
plt.ylabel('X value')

plt.subplot(3, 1, 2)
plt.plot(df['timestamp'], df['y'], color='g')
plt.title('Gyroscope Y')
plt.xlabel('Timestamp')
plt.ylabel('Y value')

plt.subplot(3, 1, 3)
plt.plot(df['timestamp'], df['z'], color='b')
plt.title('Gyroscope Z')
plt.xlabel('Timestamp')
plt.ylabel('Z value')

plt.tight_layout()
plt.show()

# Combined plot
plt.figure(figsize=(10, 5))
plt.plot(df['timestamp'], df['x'], label='X', color='r')
plt.plot(df['timestamp'], df['y'], label='Y', color='g')
plt.plot(df['timestamp'], df['z'], label='Z', color='b')
plt.title('Gyroscope X, Y, Z Combined')
plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.legend()
plt.show()
