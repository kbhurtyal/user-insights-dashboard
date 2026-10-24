import os
import pandas as pd
import plotly.express as px

os.makedirs("visuals", exist_ok=True)

# ---------- LOAD ----------
users = pd.read_csv("data/users.csv", parse_dates=["signup_date"])
events = pd.read_csv("data/events.csv", parse_dates=["timestamp"])
purchases = pd.read_csv("data/purchases.csv", parse_dates=["purchase_date"])

# ---------- CLEAN ----------
raw_rows = len(events)

events = events.drop_duplicates(subset="event_id")
purchases = purchases.drop_duplicates(subset="purchase_id")

# Standardize feature labels ("search" -> "Search", "profileview" -> "ProfileView")
canonical = {f.lower(): f for f in ["Search", "ProfileView", "Purchase", "Settings"]}
events["feature"] = events["feature"].str.lower().map(canonical)

# Drop events from users that don't exist in the users table
events = events[events["user_id"].isin(users["user_id"])]

events["date"] = events["timestamp"].dt.date

print(f"Events: {raw_rows:,} raw -> {len(events):,} after cleaning")
print(f"Missing session_duration (excluded from duration chart): {events['session_duration'].isna().sum():,}")
print(f"Missing purchase amounts (excluded from revenue): {purchases['amount'].isna().sum():,}")

# Join plan onto events
events = events.merge(users[["user_id", "plan"]], on="user_id", how="left")

# ---------- CHARTS ----------
fig1 = px.histogram(events, x="feature", title="Feature Usage Distribution")
fig1.write_html("visuals/feature_usage_distribution.html")

fig2 = px.histogram(events.dropna(subset=["session_duration"]), x="session_duration",
                    nbins=30, title="Session Duration Distribution (seconds)")
fig2.write_html("visuals/session_duration.html")

top_users = events.groupby("user_id")["actions"].sum().sort_values(ascending=False).head(10)
fig3 = px.bar(x=top_users.index, y=top_users.values,
              labels={"x": "User ID", "y": "Total Actions"}, title="Top 10 Active Users")
fig3.write_html("visuals/top_users.html")

daily = events.groupby(["date", "feature"]).size().reset_index(name="count")
fig4 = px.line(daily, x="date", y="count", color="feature", title="Feature Usage Over Time")
fig4.write_html("visuals/feature_usage_over_time.html")

# New: engagement by plan
by_plan = events.groupby(["plan", "feature"]).size().reset_index(name="count")
fig5 = px.bar(by_plan, x="plan", y="count", color="feature", barmode="group",
              title="Feature Usage by Plan")
fig5.write_html("visuals/usage_by_plan.html")

# New: revenue over time
revenue = (purchases.dropna(subset=["amount"])
           .groupby("purchase_date")["amount"].sum().reset_index())
fig6 = px.line(revenue, x="purchase_date", y="amount", title="Daily Revenue")
fig6.write_html("visuals/daily_revenue.html")

print("Saved 6 charts to the visuals folder")