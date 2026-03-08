import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from streamlit_autorefresh import st_autorefresh

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="AI Supply Chain Control Center",
    page_icon="🤖",
    layout="wide"
)

st_autorefresh(interval=10000)

# ======================
# DATABASE CONNECTION
# ======================

conn = psycopg2.connect(
    host="aws-1-ap-southeast-2.pooler.supabase.com",
    database="postgres",
    user="postgres.ctsauxidbhbejknhjjcy",
    password="Vaivasvat@2405",
    port="5432",
    sslmode="require"
)

# ======================
# LOAD DATA
# ======================

orders = pd.read_sql("SELECT * FROM orders", conn)
risk = pd.read_sql("SELECT * FROM risk_alert", conn)
recommendations = pd.read_sql("SELECT * FROM recommendation", conn)
suppliers = pd.read_sql("SELECT * FROM supplier", conn)
inventory = pd.read_sql("SELECT * FROM inventory", conn)

# ======================
# SIMULATE LIVE DELAYS
# ======================

if not orders.empty:
    random_orders = orders.sample(frac=0.1)
    orders.loc[random_orders.index, "status"] = "Delayed"

# ======================
# DYNAMIC RISK CALCULATION
# ======================

delayed_orders = len(orders[orders["status"] == "Delayed"])
delayed_ratio = delayed_orders / len(orders)

supplier_risk = 1 - suppliers["reliability_score"].mean()

inventory_risk = (inventory["reorder_point"] > inventory["stock_level"]).mean()

avg_risk = (
    delayed_ratio * 0.5
    + supplier_risk * 0.3
    + inventory_risk * 0.2
)

health_score = 1 - avg_risk

# ======================
# RISK COLOR
# ======================

risk_color = "green"

if avg_risk > 0.7:
    risk_color = "red"
elif avg_risk > 0.4:
    risk_color = "orange"

# ======================
# SIDEBAR
# ======================

st.sidebar.title("🤖 AI Control Panel")
st.sidebar.success("AI Agent Active")

# ======================
# TITLE
# ======================

st.title("AI Supply Chain Risk Manager")
st.success("AI Agent actively monitoring supply chain risks")

# ======================
# SYSTEM STATUS
# ======================

st.header("System Status")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Orders", len(orders))
col2.metric("⚠ Risk Alerts", len(risk))
col3.metric("🤖 AI Recommendations", len(recommendations))
col4.metric("🟢 Agent Status", "ACTIVE")
col5.metric("Supply Chain Health", round(health_score,2))

# ======================
# RISK GAUGE
# ======================

st.subheader("Global Supply Chain Risk Level")

col1, col2 = st.columns(2)

with col1:

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk,
        title={'text': "Risk Index"},
        gauge={
            'axis': {'range': [0,1]},
            'bar': {'color': risk_color}
        }
    ))

    st.plotly_chart(gauge, use_container_width=True)

with col2:

    fig = px.bar(
        suppliers,
        x="name",
        y="reliability_score",
        color="reliability_score",
        color_continuous_scale="RdYlGn",
        title="Supplier Reliability Scores"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# ORDERS
# ======================

st.header("Orders Overview")
st.dataframe(orders, use_container_width=True)

# ======================
# RISK ALERTS
# ======================

st.header("Risk Detection Alerts")

st.dataframe(risk, use_container_width=True)

if not risk.empty:

    risk['timestamp'] = pd.to_datetime(risk['timestamp'])

    fig = px.line(
        risk,
        x="timestamp",
        y="risk_score",
        markers=True,
        title="Supply Chain Risk Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# AI ACTIVITY FEED
# ======================

st.header("AI Activity Feed")

if not risk.empty:

    events = risk.sort_values("timestamp", ascending=False).head(10)

    for _, row in events.iterrows():
        st.write(f"⚡ {row['timestamp']} - {row['reason']} (Order {row['order_id']})")

# ======================
# AI RISK PREDICTION
# ======================

st.header("AI Risk Prediction")

if not risk.empty:

    risk_sorted = risk.sort_values("timestamp")

    risk_sorted['timestamp'] = pd.to_datetime(risk_sorted['timestamp'])
    risk_sorted['time_index'] = np.arange(len(risk_sorted))

    X = risk_sorted[['time_index']]
    y = risk_sorted['risk_score']

    model = LinearRegression()
    model.fit(X, y)

    future = np.array([[len(risk_sorted)+7]])
    predicted_risk = model.predict(future)[0]

    st.metric("Predicted Risk Score (Next 7 Days)", round(predicted_risk,2))

# ======================
# SUPPLIER RADAR
# ======================

st.header("Supplier Performance Radar")

radar = go.Figure()

for _, row in suppliers.iterrows():

    radar.add_trace(go.Scatterpolar(
        r=[
            row['reliability_score'],
            1/row['cost_index'] if row['cost_index']>0 else 0,
            1/row['avg_delivery_time'] if row['avg_delivery_time']>0 else 0
        ],
        theta=["Reliability","Cost Efficiency","Delivery Speed"],
        fill='toself',
        name=row['name']
    ))

radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,1])),
    title="Supplier Performance Comparison"
)

st.plotly_chart(radar, use_container_width=True)

# ======================
# AI RECOMMENDATIONS
# ======================

st.header("AI Supplier Recommendations")
st.dataframe(recommendations, use_container_width=True)

# ======================
# AI EXPLANATION
# ======================

st.header("AI Decision Explanation")

if not recommendations.empty:

    latest = recommendations.iloc[-1]

    st.info(
f"""
AI Decision for Order #{latest['order_id']}

Recommended Supplier ID: {latest['recommended_supplier_id']}

Estimated Delivery: {latest['estimated_delivery']} days

Estimated Cost Index: {latest['estimated_cost']}

Reason: {latest['agent_reason']}
"""
)

# ======================
# LOGISTICS MAP
# ======================

st.header("India Supply Chain Command Map")

map_data = pd.read_sql("""
SELECT o.status, l.city, l.lat, l.lon
FROM orders o
JOIN order_location l
ON o.id = l.order_id
""", conn)

fig = px.scatter_mapbox(
    map_data,
    lat="lat",
    lon="lon",
    color="status",
    hover_name="city",
    zoom=4,
    height=500
)

fig.update_layout(mapbox_style="carto-darkmatter")

st.plotly_chart(fig, use_container_width=True)

# ======================
# ANIMATED LOGISTICS FLOW
# ======================

st.header("Logistics Network Flow")

routes = pd.DataFrame({
    "from_city":["Mumbai","Delhi","Chennai","Ahmedabad"],
    "to_city":["Delhi","Bangalore","Hyderabad","Pune"],
    "lat":[19.0760,28.7041,13.0827,23.0225],
    "lon":[72.8777,77.1025,80.2707,72.5714]
})

st.map(routes)

# ======================
# CRISIS SIMULATOR
# ======================

st.header("Global Supply Chain Crisis Simulator")

crisis = st.selectbox(
    "Select Crisis Scenario",
    ["Port Shutdown","Supplier Bankruptcy","Demand Spike","Transport Strike","Natural Disaster"]
)

severity = st.slider("Crisis Severity",1,10,5)

if st.button("Run Crisis Simulation"):

    impact = severity * 0.08
    simulated_risk = avg_risk + impact

    st.warning(f"Crisis Triggered: {crisis}")

    st.metric("Simulated Risk Level", round(simulated_risk,2))

    fig = px.bar(
        x=["Before Crisis","After Crisis"],
        y=[avg_risk, simulated_risk],
        title="Supply Chain Risk Impact"
    )

    st.plotly_chart(fig)

    st.info("""
AI Response Plan

• Risk alerts generated  
• Alternative suppliers recommended  
• Logistics routes re-evaluated  
• Monitoring frequency increased
""")

conn.close()