# AI Supply Chain Risk Manager

An AI-driven supply chain monitoring system that detects operational risks, predicts disruptions, and recommends mitigation strategies.

## Project structure

```
├── dashboard.py          # Streamlit control tower (main UI)
├── requirements.txt      # Python dependencies
├── pom.xml               # Spring Boot API
├── mvnw / mvnw.cmd        # Maven wrapper
├── .env.example          # Environment variable template
└── src/
    ├── main/java/...     # REST API, entities, monitoring agent
    └── test/             # H2-backed integration tests
```

## Features

- Real-time supply chain monitoring dashboard
- AI risk detection and supplier recommendations (Spring Boot API)
- Scheduled monitoring agent for delivery delays
- Weather, fuel, and news risk signals in the dashboard

## Tech stack

| Layer     | Technology              |
| --------- | ----------------------- |
| Dashboard | Streamlit, Plotly       |
| API       | Spring Boot 3, JPA      |
| Database  | PostgreSQL (Supabase)   |
| ML        | scikit-learn (dashboard)|

## Quick start

### 1. Configure environment

Copy `.env.example` to `.env` and fill in your database and API keys.

**Dashboard** uses: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and optionally `DB_NAME`, `DB_PORT`, `DB_SSLMODE`, `OPENWEATHER_API_KEY`, `NEWS_API_KEY`, `FUEL_API_KEY`.

**API** uses: `DATABASE_URL`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `OPENWEATHER_API_KEY`.

### 2. Run the dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

### 3. Run the API (optional)

Requires Java 17+:

```bash
./mvnw spring-boot:run
```

API runs on `http://localhost:8080`. Endpoints include `/orders`, `/suppliers`, `/inventory`, `/risk`, `/recommendations`.

## Database tables

- `orders`, `supplier`, `inventory`, `risk_alert`, `recommendation`
- `order_location` (optional, for the India logistics map)
