import os 
import numpy as np
import pandas as pd 

rng = np.random.default_rng(42)

# Parameters
NUM_USERS = 500
NUM_EVENTS = 50_000
START = pd.Timestamp("2025-06-01")
END = pd.Timestamp("2025-09-30")

FEATURES = ["Search", "ProfileView", "Purchase", "Settings"]
FEATURE_WEIGHTS = [0.45, 0.30, 0.10, 0.15]
PLANS = ["Free", "Pro", "Enterprise"]
PLAN_WEIGHTS = [0.70, 0.25, 0.05]
COUNTRIES = ["US", "Canada", "UK", "India", "Germany", "Australia"]
COUNTRY_WEIGHTS = [0.50, 0.10, 0.12, 0.15, 0.08, 0.05]

# ---------- USERS ----------
user_ids = np.array([f"U{i:04d}" for i in range(1, NUM_USERS + 1)])
signup_days = rng.integers(0, (END - START).days - 14, NUM_USERS)
users = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": START + pd.to_timedelta(signup_days, unit="D"),
    "plan": rng.choice(PLANS, NUM_USERS, p=PLAN_WEIGHTS),
    "country": rng.choice(COUNTRIES, NUM_USERS, p=COUNTRY_WEIGHTS),
})

# ---------- EVENTS ----------
# A few power users generate most of the activity
user_weights = rng.pareto(a=1.5, size=NUM_USERS) + 1
user_weights = user_weights / user_weights.sum()
event_users = rng.choice(user_ids, NUM_EVENTS, p=user_weights)

# Events happen after the user signed up
signup_lookup = users.set_index("user_id")["signup_date"]
signup_ts = signup_lookup.loc[event_users].to_numpy()
span_seconds = (END - pd.to_datetime(signup_ts)).total_seconds().to_numpy()
offsets = rng.random(NUM_EVENTS) * span_seconds
timestamps = pd.to_datetime(signup_ts) + pd.to_timedelta(offsets, unit="s")

events = pd.DataFrame({
    "user_id": event_users,
    "timestamp": timestamps.floor("s"),
    "feature": rng.choice(FEATURES, NUM_EVENTS, p=FEATURE_WEIGHTS),
    "session_duration": rng.gamma(2.0, 150, NUM_EVENTS).round().astype(int).clip(30, 1800),
    "actions": rng.poisson(5, NUM_EVENTS) + 1,
})
events = events.sort_values("timestamp").reset_index(drop=True)
events.insert(0, "event_id", [f"E{i:06d}" for i in range(1, len(events) + 1)])
events["date"] = events["timestamp"].dt.date

# ---------- PURCHASES (built from clean Purchase events) ----------
buys = events[events["feature"] == "Purchase"]
plan_lookup = users.set_index("user_id")["plan"]
plan_multiplier = buys["user_id"].map(plan_lookup).map(
    {"Free": 1.0, "Pro": 2.5, "Enterprise": 6.0}
).to_numpy()
purchases = pd.DataFrame({
    "purchase_id": [f"P{i:06d}" for i in range(1, len(buys) + 1)],
    "user_id": buys["user_id"].to_numpy(),
    "purchase_date": buys["date"].to_numpy(),
    "amount": (rng.lognormal(3.2, 0.6, len(buys)) * plan_multiplier).round(2),
})

# ---------- INJECT REALISTIC DATA QUALITY PROBLEMS ----------
# 1. Duplicate event rows (~1%)
dupes = events.sample(frac=0.01, random_state=1)
events = pd.concat([events, dupes]).sort_values("timestamp").reset_index(drop=True)

# 2. Missing session durations (~2%)
missing_idx = events.sample(frac=0.02, random_state=2).index
events.loc[missing_idx, "session_duration"] = np.nan

# 3. Inconsistent feature labels (~3%)
messy_idx = events.sample(frac=0.03, random_state=3).index
events.loc[messy_idx, "feature"] = events.loc[messy_idx, "feature"].str.lower()

# 4. Orphan user IDs that don't exist in users (~0.5%)
orphan_idx = events.sample(frac=0.005, random_state=4).index
events.loc[orphan_idx, "user_id"] = "U9999"

# 5. Purchases: missing amounts (~2%) and duplicate rows (~1%)
purchases.loc[purchases.sample(frac=0.02, random_state=5).index, "amount"] = np.nan
purchases = pd.concat([purchases, purchases.sample(frac=0.01, random_state=6)])

# ---------- SAVE ----------
os.makedirs("data", exist_ok=True)
users.to_csv("data/users.csv", index=False)
events.to_csv("data/events.csv", index=False)
purchases.to_csv("data/purchases.csv", index=False)

print(f"users: {len(users):,} | events: {len(events):,} | purchases: {len(purchases):,}")