# User Insights Dashboard

A data analytics project that simulates user behavior and visualizes key usage trends using Python, Pandas, and Plotly.

## Features

- **Feature Usage Distribution**: Identify the most used features.
- **Session Duration Histogram**: Understand how long users stay active.
- **Top 10 Users by Actions**: See who your most engaged users are.
- **Feature Usage Over Time**: Spot trends and usage patterns over time.

## Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Jupyter Notebook

## Dataset

Simulated data with the following fields:
- `user_id`: Unique user identifier
- `feature`: Feature interacted with (`click`, `search`, `purchase`, etc.)
- `timestamp`: Activity time
- `session_duration`: Duration of session (in minutes)
- `actions`: Count of actions in a session

## Usage

1. Clone the repo
2. Create a virtual environment and install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Open the notebook and run all cells:
   ```
   jupyter notebook UserInsightsDashboard.ipynb
   ```

## Output

All interactive dashboards will be rendered using Plotly. Optionally, export them to `.html`.

## License

MIT
