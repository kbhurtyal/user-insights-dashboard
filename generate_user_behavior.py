import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create output folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Parameters
num_rows = 100
start_date = datetime(2025, 7, 1)
features = ["Search", "ProfileView", "Purchase", "Settings"]
user_ids = [f"U{str(i).zfill(3)}" for i in range(1, 21)]

# Generate data
data = []
for _ in range(num_rows):
    user_id = random.choice(user_ids)
    timestamp = start_date + timedelta(
        days=random.randint(0, 10),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    feature = random.choice(features)
    session_duration = random.randint(60, 600)
    actions = random.randint(1, 12)
    date_only = timestamp.date()
    data.append([user_id, timestamp, feature, session_duration, actions, date_only])

df = pd.DataFrame(data, columns=[
    "user_id", "timestamp", "feature", "session_duration", "actions", "date"
])
df.to_csv("data/user_behavior.csv", index=False)
print("✅ Data saved to data/user_behavior.csv")
