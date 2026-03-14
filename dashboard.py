import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import numpy as np
import random
import requests
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

st_autorefresh(interval=60000)

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
# WEATHER API
# ======================

weather = "Unknown"
temp = 0
humidity = 0
weather_risk = 0

try:
    API_KEY = "8a1db6e978cc9a38edbe3d1391e178e3"

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    weather = data["weather"][0]["main"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

except:
    weather = "Unavailable"

# ======================
# WEATHER RISK
# ======================

if weather in ["Rain", "Thunderstorm"]:
    weather_risk = 0.15
elif weather in ["Snow", "Extreme"]:
    weather_risk = 0.25
elif weather in ["Clouds"]:
    weather_risk = 0.05
else:
    weather_risk = 0

# ======================
# SUPPLY CHAIN NEWS API
# ======================

news_list = []

try:
    NEWS_API_KEY = "f5e7262e4dd048ad9096e6a6974fe83d"

    news_url = f"https://newsapi.org/v2/everything?q=supply chain OR logistics OR port strike&sortBy=publishedAt&apiKey={NEWS_API_KEY}"

    news_response = requests.get(news_url)
    news_data = news_response.json()

    for article in news_data.get("articles", [])[:5]:
        news_list.append(article["title"])

except:
    news_list = []

# ======================
# FUEL API
# ======================

fuel_price = 0
fuel_risk = 0

try:
    FUEL_API_KEY = "HCJ6OYW037L40QK0"

    fuel_url = f"https://www.alphavantage.co/query?function=BRENT&interval=daily&apikey={FUEL_API_KEY}"

    fuel_response = requests.get(fuel_url)
    fuel_data = fuel_response.json()

    if "data" in fuel_data:
        fuel_price = float(fuel_data["data"][0]["value"])

except:
    fuel_price = 0

# ======================
# FUEL RISK
# ======================

if fuel_price > 90:
    fuel_risk = 0.15
elif fuel_price > 75:
    fuel_risk = 0.08
else:
    fuel_risk = 0.03

# ======================
# VESSEL TRACKING DATA
# ======================

vessels = pd.DataFrame({
    "ship":["MSC Aurora","Maersk Atlanta","Evergreen Pacific","Hapag Lloyd Star"],
    "lat":[18.5,19.2,16.8,21.1],
    "lon":[72.8,73.1,71.9,72.4],
    "status":["In Transit","Docking","Delayed","In Transit"]
})

shipping_risk = 0
if "Delayed" in vessels["status"].values:
    shipping_risk = 0.05

# ======================
# SIMULATE DELAYS
# ======================

if not orders.empty:
    random_orders = orders.sample(frac=0.1)
    orders.loc[random_orders.index,"status"] = "Delayed"

# ======================
# RISK CALCULATION
# ======================

delayed_orders = len(orders[orders["status"]=="Delayed"])
delayed_ratio = delayed_orders / len(orders) if len(orders)>0 else 0

supplier_risk = 1 - suppliers["reliability_score"].mean()
inventory_risk = (inventory["reorder_point"] > inventory["stock_level"]).mean()

avg_risk = (
    delayed_ratio * 0.35
    + supplier_risk * 0.25
    + inventory_risk * 0.2
    + weather_risk * 0.1
    + fuel_risk * 0.05
    + shipping_risk * 0.05
)

health_score = 1 - avg_risk

risk_color="green"
if avg_risk>0.7:
    risk_color="red"
elif avg_risk>0.4:
    risk_color="orange"

# ======================
# SIDEBAR
# ======================

st.sidebar.title("🤖 AI Control Panel")
st.sidebar.success("AI Agent Active")

st.sidebar.markdown("---")
st.sidebar.subheader("System Monitor")
st.sidebar.metric("API Status","Online")
st.sidebar.metric("Database","Connected")
st.sidebar.metric("Last Update","Live")

# ======================
# TITLE
# ======================

st.title("AI Supply Chain Risk Manager")
st.success("AI Agent actively monitoring supply chain risks")

# ======================
# WEATHER
# ======================

st.header("🌦 Logistics Weather Monitor")

c1,c2,c3 = st.columns(3)
c1.metric("Weather",weather)
c2.metric("Temperature",round(temp,2))
c3.metric("Humidity",humidity)

# ======================
# FUEL
# ======================

st.header("⛽ Global Fuel Price Monitor")

c1,c2 = st.columns(2)

c1.metric("Brent Crude Price ($)",fuel_price)

fuel_status="Stable"
if fuel_price>90:
    fuel_status="High Transport Cost Risk"
elif fuel_price>75:
    fuel_status="Moderate Risk"

c2.metric("Fuel Risk Status",fuel_status)

# ======================
# NEWS
# ======================

st.header("🌍 Global Supply Chain Disruption Monitor")

if news_list:
    for item in news_list:
        st.warning(item)
else:
    st.info("No major disruptions detected")

# ======================
# SYSTEM STATUS
# ======================

st.header("System Status")

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Orders",len(orders))
c2.metric("Risk Alerts",len(risk))
c3.metric("AI Recommendations",len(recommendations))
c4.metric("Agent Status","ACTIVE")
c5.metric("Supply Chain Health",round(health_score,2))

# ======================
# GLOBAL HEATMAP
# ======================

st.header("🌎 Global Risk Heatmap")

risk_map = pd.DataFrame({
    "city":["Mumbai","Delhi","Chennai","Ahmedabad","Bangalore"],
    "lat":[19.0760,28.7041,13.0827,23.0225,12.9716],
    "lon":[72.8777,77.1025,80.2707,72.5714,77.5946],
    "risk":[0.4,0.6,0.2,0.5,0.3]
})

fig = px.scatter_mapbox(
    risk_map,
    lat="lat",
    lon="lon",
    size="risk",
    color="risk",
    zoom=3,
    height=450,
    color_continuous_scale="Reds"
)

fig.update_layout(mapbox_style="carto-darkmatter")
st.plotly_chart(fig,use_container_width=True)

# ======================
# RISK GAUGE
# ======================

st.subheader("Global Supply Chain Risk Level")

col1,col2 = st.columns(2)

with col1:
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk,
        title={'text':"Risk Index"},
        gauge={'axis':{'range':[0,1]},'bar':{'color':risk_color}}
    ))
    st.plotly_chart(gauge,use_container_width=True)

with col2:
    fig = px.bar(
        suppliers,
        x="name",
        y="reliability_score",
        color="reliability_score",
        color_continuous_scale="RdYlGn"
    )
    st.plotly_chart(fig,use_container_width=True)

# ======================
# ORDERS
# ======================

st.header("Orders Overview")
st.dataframe(orders,use_container_width=True)

# ======================
# RISK ALERTS
# ======================

st.header("Risk Detection Alerts")

st.dataframe(risk,use_container_width=True)

if not risk.empty:
    risk['timestamp']=pd.to_datetime(risk['timestamp'])
    fig = px.line(risk,x="timestamp",y="risk_score",markers=True)
    st.plotly_chart(fig,use_container_width=True)

# ======================
# AI ACTIVITY FEED
# ======================

st.header("AI Activity Feed")

if not risk.empty:
    events = risk.sort_values("timestamp",ascending=False).head(10)
    for _,row in events.iterrows():
        st.write(f"⚡ {row['timestamp']} - {row['reason']} (Order {row['order_id']})")

# ======================
# AI RISK PREDICTION
# ======================

st.header("AI Risk Prediction")

if not risk.empty:

    risk_sorted = risk.sort_values("timestamp")
    risk_sorted['timestamp']=pd.to_datetime(risk_sorted['timestamp'])
    risk_sorted['time_index']=np.arange(len(risk_sorted))

    X = risk_sorted[['time_index']]
    y = risk_sorted['risk_score']

    model = LinearRegression()
    model.fit(X,y)

    future = np.array([[len(risk_sorted)+7]])
    predicted_risk = model.predict(future)[0]

    st.metric("Predicted Risk Score (Next 7 Days)",round(predicted_risk,2))

# ======================
# SUPPLIER RADAR
# ======================

st.header("Supplier Performance Radar")

radar = go.Figure()

for _,row in suppliers.iterrows():

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
    polar=dict(radialaxis=dict(visible=True,range=[0,1])),
    title="Supplier Performance Comparison"
)

st.plotly_chart(radar,use_container_width=True)

# ======================
# SHIPPING MONITOR
# ======================

st.header("🚢 Global Shipping Activity Monitor")

ship_map = px.scatter_mapbox(
    vessels,
    lat="lat",
    lon="lon",
    color="status",
    hover_name="ship",
    zoom=3,
    height=400
)

ship_map.update_layout(mapbox_style="carto-darkmatter")
st.plotly_chart(ship_map,use_container_width=True)

# ======================
# INDIA LOGISTICS MAP
# ======================

st.header("India Supply Chain Command Map")

map_data = pd.read_sql("""
SELECT o.status,l.city,l.lat,l.lon
FROM orders o
JOIN order_location l
ON o.id = l.order_id
""",conn)

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
st.plotly_chart(fig,use_container_width=True)

conn.close()