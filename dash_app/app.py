import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import re

# =====================================================
# DATABASE CONNECTION
# =====================================================
engine = create_engine(
    "postgresql+psycopg2://postgres:newpassword@localhost:5432/sunrise_db"
)

def load_data():
    return pd.read_sql("SELECT * FROM sun_cycle", engine)

df = load_data()
df["city"] = df["city"].astype(str)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

def convert_duration(x):
    match = re.search(r"(\d+)\s*h.*?(\d+)\s*m", str(x))
    if match:
        h, m = match.groups()
        return int(h) + int(m) / 60
    return None

df["daylight_hours"] = df["daylight_duration"].apply(convert_duration)

df["time_remaining_hours"] = (
    df["time_remaining"]
    .astype(str)
    .str.extract(r"(\d+)")[0]
    .astype(float)
)

# normalize city filtering
df["city_lower"] = df["city"].str.lower()

# clean next_event display values
df["next_event"] = (
    df["next_event"]
    .astype(str)
    .str.replace("_", " ")
    .str.title()
)

# =====================================================
# APP INIT
# =====================================================
app = dash.Dash(__name__)
app.title = "Sun Analytics Dashboard"

# =====================================================
# LAYOUT
# =====================================================
app.layout = html.Div([

    html.H1("🌅 Sunrise & Sunset Analytics Dashboard"),

    # -------------------------
    # FILTER
    # -------------------------
    dcc.Dropdown(
        id="city",
        options=[{"label": c, "value": c} for c in df["city"].unique()],
        value=df["city"].iloc[0],
        clearable=False
    ),

    html.Hr(),

    # -------------------------
    # KPI CARD
    # -------------------------
    html.Div(id="kpi"),

    html.Br(),

    # -------------------------
    # CHARTS
    # -------------------------
    dcc.Graph(id="chart1"),
    dcc.Graph(id="chart2")
])

# =====================================================
# CALLBACK
# =====================================================
@app.callback(
    Output("kpi", "children"),
    Output("chart1", "figure"),
    Output("chart2", "figure"),
    Input("city", "value")
)
def update(city):

    filtered = df[df["city_lower"] == city.lower()]

    if filtered.empty:
        return (
            html.Div("No data found"),
            px.bar(title="No data"),
            px.bar(title="No data")
        )

    row = filtered.iloc[0]

    # -------------------------
    # KPI
    # -------------------------
    kpi = html.Div([
        html.H3("📊 Key Metrics"),

        html.P(f"Sunrise: {row['sunrise']}"),
        html.P(f"Sunset: {row['sunset']}"),
        html.P(f"Daylight Duration: {row['daylight_duration']}"),

        html.P(f"Next Event: {row['next_event']}"),
        html.P(f"Time Until Next Event: {row['time_remaining']}")
    ])

    # -------------------------
    # CHART 1
    # -------------------------
    fig1 = px.bar(
        filtered,
        x="city",
        y="daylight_hours",
        title="Daylight Duration by City",
    )

    fig1.update_layout(
        xaxis_title="City",
        yaxis_title="Daylight hours"
    )

    # -------------------------
    # CHART 2
    # -------------------------
    fig2 = px.bar(
        filtered,
        x="city",
        y="time_remaining_hours",
        color="next_event",
        title="Time Remaining Until Next Solar Event",
        labels={
            "next_event": "Next Event"
        }
    )

    fig2.update_layout(
        xaxis_title="City",
        yaxis_title="Time remaining (hours)"
    )

    return kpi, fig1, fig2

# =====================================================
# RUN APP
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)