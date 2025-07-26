import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("data/user_behavior.csv", parse_dates=["timestamp"])

# 1. Feature usage distribution
fig1 = px.histogram(df, x="feature", title="Feature Usage Distribution")
fig1.show()

# 2. Session duration analysis
fig2 = px.histogram(df, x="session_duration", nbins=20, title="Session Duration Distribution (seconds)")
fig2.show()

# 3. Top 10 most active users
user_activity = df.groupby("user_id")["actions"].sum().sort_values(ascending=False).head(10)
fig3 = px.bar(user_activity, x=user_activity.index, y=user_activity.values, labels={"x": "User ID", "y": "Total Actions"}, title="Top 10 Active Users")
fig3.show()

# 4. Feature usage trend over time
daily_usage = df.groupby(["date", "feature"]).size().reset_index(name="count")
fig4 = px.line(daily_usage, x="date", y="count", color="feature", title="Feature Usage Over Time")
fig4.show()
