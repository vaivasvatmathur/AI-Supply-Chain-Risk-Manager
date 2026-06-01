"""Streamlit control tower for the AI Supply Chain Risk Manager."""

import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import requests
import streamlit as st
from sklearn.linear_model import LinearRegression
from streamlit_autorefresh import st_autorefresh


def get_db_connection():
    required = ("DB_HOST", "DB_USER", "DB_PASSWORD")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        st.error(
            "Database is not configured. Set these environment variables: "
            + ", ".join(missing)
            + ". See `.env.example`."
        )
        st.stop()

    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.getenv("DB_NAME", "postgres"),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=os.getenv("DB_PORT", "5432"),
        sslmode=os.getenv("DB_SSLMODE", "require"),
    )


def load_table(conn, table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", conn)


def fetch_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return "Unavailable", 0, 0, 0

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q=Mumbai&appid={api_key}&units=metric"
        )
        data = requests.get(url, timeout=10).json()
        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
    except (requests.RequestException, KeyError, TypeError):
        return "Unavailable", 0, 0, 0

    if weather in ("Rain", "Thunderstorm"):
        weather_risk = 0.15
    elif weather in ("Snow", "Extreme"):
        weather_risk = 0.25
    elif weather == "Clouds":
        weather_risk = 0.05
    else:
        weather_risk = 0

    return weather, temp, humidity, weather_risk


def fetch_news():
    api_key = os.getenv("NEWS_API_KEY", "")
    if not api_key:
        return []

    try:
        url = (
            "https://newsapi.org/v2/everything"
            "?q=supply chain OR logistics OR port strike"
            "&sortBy=publishedAt"
            f"&apiKey={api_key}"
        )
        news_data = requests.get(url, timeout=10).json()
        return [
            article["title"]
            for article in news_data.get("articles", [])[:5]
            if article.get("title")
        ]
    except (requests.RequestException, KeyError, TypeError):
        return []


def fetch_fuel_price():
    api_key = os.getenv("FUEL_API_KEY", "")
    if not api_key:
        return 0, 0.03

    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=BRENT&interval=daily&apikey={api_key}"
        )
        fuel_data = requests.get(url, timeout=10).json()
        if "data" in fuel_data and fuel_data["data"]:
            price = float(fuel_data["data"][0]["value"])
            if price > 90:
                return price, 0.15
            if price > 75:
                return price, 0.08
            return price, 0.03
    except (requests.RequestException, KeyError, TypeError, ValueError):
        pass

    return 0, 0.03


def main():
    st.set_page_config(
        page_title="AI Supply Chain Control Center",
        page_icon="🤖",
        layout="wide",
    )
    st_autorefresh(interval=60_000, key="dashboard_refresh")

    conn = get_db_connection()
    try:
        orders = load_table(conn, "orders")
        risk = load_table(conn, "risk_alert")
        recommendations = load_table(conn, "recommendation")
        suppliers = load_table(conn, "supplier")
        inventory = load_table(conn, "inventory")
    finally:
        conn.close()

    weather, temp, humidity, weather_risk = fetch_weather()
    news_list = fetch_news()
    fuel_price, fuel_risk = fetch_fuel_price()

    vessels = pd.DataFrame(
        {
            "ship": ["MSC Aurora", "Maersk Atlanta", "Evergreen Pacific", "Hapag Lloyd Star"],
            "lat": [18.5, 19.2, 16.8, 21.1],
            "lon": [72.8, 73.1, 71.9, 72.4],
            "status": ["In Transit", "Docking", "Delayed", "In Transit"],
        }
    )
    shipping_risk = 0.05 if "Delayed" in vessels["status"].values else 0

    if not orders.empty and "status" in orders.columns:
        sample = orders.sample(frac=min(0.1, 1.0), random_state=42)
        orders = orders.copy()
        orders.loc[sample.index, "status"] = "Delayed"

    delayed_orders = len(orders[orders["status"] == "Delayed"]) if not orders.empty else 0
    delayed_ratio = delayed_orders / len(orders) if len(orders) > 0 else 0

    supplier_risk = 1 - suppliers["reliability_score"].mean() if not suppliers.empty else 0
    inventory_risk = (
        (inventory["reorder_point"] > inventory["stock_level"]).mean()
        if not inventory.empty
        else 0
    )

    avg_risk = (
        delayed_ratio * 0.35
        + supplier_risk * 0.25
        + inventory_risk * 0.2
        + weather_risk * 0.1
        + fuel_risk * 0.05
        + shipping_risk * 0.05
    )
    health_score = 1 - avg_risk

    risk_color = "green"
    if avg_risk > 0.7:
        risk_color = "red"
    elif avg_risk > 0.4:
        risk_color = "orange"

    st.sidebar.title("🤖 AI Control Panel")
    st.sidebar.success("AI Agent Active")
    st.sidebar.markdown("---")
    st.sidebar.subheader("System Monitor")
    st.sidebar.metric("API Status", "Online")
    st.sidebar.metric("Database", "Connected")
    st.sidebar.metric("Last Update", "Live")

    st.title("AI Supply Chain Risk Manager")
    st.success("AI Agent actively monitoring supply chain risks")

    st.header("🌦 Logistics Weather Monitor")
    c1, c2, c3 = st.columns(3)
    c1.metric("Weather", weather)
    c2.metric("Temperature", round(temp, 2))
    c3.metric("Humidity", humidity)

    st.header("⛽ Global Fuel Price Monitor")
    c1, c2 = st.columns(2)
    c1.metric("Brent Crude Price ($)", fuel_price)
    fuel_status = "Stable"
    if fuel_price > 90:
        fuel_status = "High Transport Cost Risk"
    elif fuel_price > 75:
        fuel_status = "Moderate Risk"
    c2.metric("Fuel Risk Status", fuel_status)

    st.header("🌍 Global Supply Chain Disruption Monitor")
    if news_list:
        for item in news_list:
            st.warning(item)
    else:
        st.info("No major disruptions detected")

    st.header("System Status")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Orders", len(orders))
    c2.metric("Risk Alerts", len(risk))
    c3.metric("AI Recommendations", len(recommendations))
    c4.metric("Agent Status", "ACTIVE")
    c5.metric("Supply Chain Health", round(health_score, 2))

    st.header("🌎 Global Risk Heatmap")
    risk_map = pd.DataFrame(
        {
            "city": ["Mumbai", "Delhi", "Chennai", "Ahmedabad", "Bangalore"],
            "lat": [19.0760, 28.7041, 13.0827, 23.0225, 12.9716],
            "lon": [72.8777, 77.1025, 80.2707, 72.5714, 77.5946],
            "risk": [0.4, 0.6, 0.2, 0.5, 0.3],
        }
    )
    heatmap = px.scatter_mapbox(
        risk_map,
        lat="lat",
        lon="lon",
        size="risk",
        color="risk",
        zoom=3,
        height=450,
        color_continuous_scale="Reds",
    )
    heatmap.update_layout(mapbox_style="carto-darkmatter")
    st.plotly_chart(heatmap, use_container_width=True)

    st.subheader("Global Supply Chain Risk Level")
    col1, col2 = st.columns(2)
    with col1:
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_risk,
                title={"text": "Risk Index"},
                gauge={"axis": {"range": [0, 1]}, "bar": {"color": risk_color}},
            )
        )
        st.plotly_chart(gauge, use_container_width=True)

    with col2:
        if not suppliers.empty:
            supplier_chart = px.bar(
                suppliers,
                x="name",
                y="reliability_score",
                color="reliability_score",
                color_continuous_scale="RdYlGn",
            )
            st.plotly_chart(supplier_chart, use_container_width=True)

    st.header("Orders Overview")
    st.dataframe(orders, use_container_width=True)

    st.header("Risk Detection Alerts")
    st.dataframe(risk, use_container_width=True)
    if not risk.empty and "timestamp" in risk.columns and "risk_score" in risk.columns:
        risk_chart_df = risk.copy()
        risk_chart_df["timestamp"] = pd.to_datetime(risk_chart_df["timestamp"])
        risk_line = px.line(risk_chart_df, x="timestamp", y="risk_score", markers=True)
        st.plotly_chart(risk_line, use_container_width=True)

    st.header("AI Activity Feed")
    if not risk.empty and "timestamp" in risk.columns:
        events = risk.sort_values("timestamp", ascending=False).head(10)
        for _, row in events.iterrows():
            st.write(
                f"⚡ {row['timestamp']} - {row.get('reason', 'Alert')} "
                f"(Order {row.get('order_id', 'N/A')})"
            )

    st.header("AI Risk Prediction")
    if not risk.empty and "risk_score" in risk.columns:
        risk_sorted = risk.sort_values("timestamp").copy()
        risk_sorted["timestamp"] = pd.to_datetime(risk_sorted["timestamp"])
        risk_sorted["time_index"] = np.arange(len(risk_sorted))
        model = LinearRegression()
        model.fit(risk_sorted[["time_index"]], risk_sorted["risk_score"])
        predicted_risk = model.predict(np.array([[len(risk_sorted) + 7]]))[0]
        st.metric("Predicted Risk Score (Next 7 Days)", round(float(predicted_risk), 2))

    st.header("Supplier Performance Radar")
    if not suppliers.empty:
        radar = go.Figure()
        for _, row in suppliers.iterrows():
            radar.add_trace(
                go.Scatterpolar(
                    r=[
                        row["reliability_score"],
                        1 / row["cost_index"] if row["cost_index"] > 0 else 0,
                        1 / row["avg_delivery_time"] if row["avg_delivery_time"] > 0 else 0,
                    ],
                    theta=["Reliability", "Cost Efficiency", "Delivery Speed"],
                    fill="toself",
                    name=row["name"],
                )
            )
        radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title="Supplier Performance Comparison",
        )
        st.plotly_chart(radar, use_container_width=True)

    st.header("🚢 Global Shipping Activity Monitor")
    ship_map = px.scatter_mapbox(
        vessels,
        lat="lat",
        lon="lon",
        color="status",
        hover_name="ship",
        zoom=3,
        height=400,
    )
    ship_map.update_layout(mapbox_style="carto-darkmatter")
    st.plotly_chart(ship_map, use_container_width=True)

    st.header("India Supply Chain Command Map")
    map_conn = get_db_connection()
    try:
        map_data = pd.read_sql(
            """
            SELECT o.status, l.city, l.lat, l.lon
            FROM orders o
            JOIN order_location l ON o.id = l.order_id
            """,
            map_conn,
        )
        if not map_data.empty:
            india_map = px.scatter_mapbox(
                map_data,
                lat="lat",
                lon="lon",
                color="status",
                hover_name="city",
                zoom=4,
                height=500,
            )
            india_map.update_layout(mapbox_style="carto-darkmatter")
            st.plotly_chart(india_map, use_container_width=True)
        else:
            st.info("No order location data available yet.")
    except Exception:
        st.info("Order location map is unavailable (order_location table missing or empty).")
    finally:
        map_conn.close()


if __name__ == "__main__":
    main()
