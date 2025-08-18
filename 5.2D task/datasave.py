from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Connect to MongoDB Atlas
# -----------------------------
mongo_client = MongoClient(
    "mongodb+srv://meinhoonayush:Mona%401973@cluster0.jmahznh.mongodb.net/?retryWrites=true&w=majority"
)
db1 = mongo_client["GyroDB"]
collection1 = db1["gyro_data"]

# -----------------------------
# 2. Read all data from MongoDB
# -----------------------------
cursor = collection1.find()
data_list = list(cursor)

# Convert to DataFrame
df = pd.DataFrame(data_list)
if "_id" in df.columns:
    df = df.drop(columns=["_id"])

# -----------------------------
# 3. Save CSV
# -----------------------------
df.to_csv("gyro_data.csv", index=False)
print("Data saved to gyro_data.csv")

# -----------------------------
# 4. Optional: Clean and plot
# -----------------------------
df[['x','y','z']] = df[['x','y','z']].apply(pd.to_numeric, errors='coerce')
df = df.dropna()
df.to_csv("gyro_data_clean.csv", index=False)

plt.figure()
plt.plot(df['timestamp'], df['x'], label='X')
plt.plot(df['timestamp'], df['y'], label='Y')
plt.plot(df['timestamp'], df['z'], label='Z')
plt.legend()
plt.show()
