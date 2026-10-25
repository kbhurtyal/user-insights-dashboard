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
def save(fig, name):
    fig.update_layout(template="plotly_white", title_x=0.5)
    fig.write_html(f"visuals/{name}.html")
    fig.write_image(f"visuals/{name}.png", width=1000, height=600, scale=2)

# 1. Feature usage
feature_counts = events["feature"].value_counts().reset_index()
feature_counts.columns = ["feature", "events"]
fig1 = px.bar(feature_counts, x="feature", y="events",
              title="Feature Usage Distribution", text="events")
save(fig1, "feature_usage")

# 2. Session duration
fig2 = px.histogram(events.dropna(subset=["session_duration"]),
                    x="session_duration", nbins=30,
                    title="Session Duration Distribution (seconds)")
save(fig2, "session_duration")

# 3. Top 10 users
top_users = events.groupby("user_id")["actions"].sum().sort_values(ascending=False).head(10)
fig3 = px.bar(x=top_users.index, y=top_users.values,
              labels={"x": "User ID", "y": "Total Actions"},
              title="Top 10 Active Users")
save(fig3, "top_users")

# 4. Usage over time
daily = events.groupby(["date", "feature"]).size().reset_index(name="count")
fig4 = px.line(daily, x="date", y="count", color="feature",
               title="Feature Usage Over Time")
save(fig4, "usage_over_time")

# 5. Usage by plan
by_plan = events.groupby(["plan", "feature"]).size().reset_index(name="count")
fig5 = px.bar(by_plan, x="plan", y="count", color="feature", barmode="group",
              title="Feature Usage by Plan")
save(fig5, "usage_by_plan")

# 6. Daily revenue
revenue = (purchases.dropna(subset=["amount"])
           .groupby("purchase_date")["amount"].sum().reset_index())
fig6 = px.line(revenue, x="purchase_date", y="amount", markers=True,
               labels={"purchase_date": "Date", "amount": "Revenue ($)"},
               title="Daily Revenue")
save(fig6, "daily_revenue")

print("Saved charts (.html and .png) to the visuals folder")