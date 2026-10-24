# User Insights Dashboard

An end-to-end analytics project that generates a simulated product dataset, cleans it, and turns it into interactive charts to explain user behavior: feature usage, engagement, and revenue.

> **Note:** All data is simulated. The project demonstrates methodology (data cleaning, validation, and analysis), not real user behavior.

## What it does

1. **Generates data** for three related tables (users, events, purchases) with realistic patterns, such as a few power users driving most activity.
2. **Injects real-world data problems** on purpose: duplicate rows, missing values, inconsistent labels, and orphan user IDs.
3. **Cleans and validates** the data, reporting what was removed or excluded.
4. **Visualizes** the results with interactive Plotly charts.
5. [**Analyzes with SQL** using DuckDB: DAU, week-over-week growth, cohort retention, revenue per user. Delete this line if you haven't added `sql_analysis.py`.]

## Data quality results

| Check | Result |
|---|---|
| Raw events | 50,500 |
| Events after removing duplicates and orphan user IDs | 49,749 |
| Missing session durations (excluded from duration chart) | 995 |
| Missing purchase amounts (excluded from revenue) | 100 |

## Charts

![Feature usage](visuals/feature_usage.png)
![Usage over time](visuals/usage_over_time.png)

[Add 2 to 4 screenshots. Interactive versions are in the `visuals/` folder.]

## Key findings

[Write 3 to 4 findings that match what your charts and SQL actually show, for example:]
- [Search is the most-used feature, at about X% of events]
- [A small share of users generate Y% of all actions]
- [Enterprise users generate the most revenue per user]

## Tech stack

Python 3, Pandas, NumPy, Plotly, [DuckDB (SQL)]

## Project structure

```
data/                          generated CSVs (users, events, purchases)
visuals/                       saved charts
generate_user_behavior.py      creates the simulated dataset
user_insights_dashboard.py     cleans data and builds charts
[sql_analysis.py]              SQL metrics with DuckDB
requirements.txt
```

## How to run

```bash
git clone https://github.com/kbhurtyal/user-insights-dashboard.git
cd user-insights-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 generate_user_behavior.py
python3 user_insights_dashboard.py
```

## Possible next steps

- Add automated data validation checks (Great Expectations)
- Build an interactive Streamlit version with filters
- Simulate and analyze an A/B test