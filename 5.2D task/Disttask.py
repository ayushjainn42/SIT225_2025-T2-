import paho.mqtt.client as mqtt
import json
import time
from pymongo import MongoClient
from urllib.parse import quote_plus  # for encoding username/password

# -------------------
# MongoDB Atlas setup
# -------------------
username = quote_plus("meinhoonayush")  # your MongoDB username
password = quote_plus("Mona@1973")     # your MongoDB password (encoded)
mongo_client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.jmahznh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db1 = mongo_client["GyroDB"]             # database name
collection1 = db1["gyro_data"]           # collection name

# -------------------
# HiveMQ Broker setup
# -------------------
broker = "f5e7e9613317481bbc8ad4efc9918939.s1.eu.hivemq.cloud"
port = 8883
topic = "nano33/gyroscope"
username_mqtt = "meinhoonayush"
password_mqtt = "Mona@1973"

# -------------------
# MQTT callback
# -------------------
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload["timestamp"] = time.time()  # add timestamp
        print("Received:", payload)

        # Store to MongoDB
        collection1.insert_one(payload)

    except Exception as e:
        print("Error:", e)

# -------------------
# MQTT client setup
# -------------------
client = mqtt.Client()
client.username_pw_set(username_mqtt, password_mqtt)
client.tls_set()  # Enable SSL/TLS
client.on_message = on_message

print("Connecting to broker...")
client.connect(broker, port, 60)
client.subscribe(topic)
print("Subscribed to topic:", topic)

# Keep listening forever
client.loop_forever()
