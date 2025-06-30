# Ubiety IoT Device Status Service

A modern, production-ready backend for tracking IoT device status, built with **FastAPI**, **PostgreSQL**, **Docker**, **Prometheus**, and **Grafana**.

---

## Features
- **FastAPI** REST API for device status updates and queries
- **PostgreSQL** for persistent storage
- **Prometheus** metrics for observability
- **Grafana** dashboards for real-time visualization
- **Docker Compose** for easy local development
- **API key** authentication for all endpoints

---

## Quick Start

### 1. Clone and Start the Stack
```sh
git clone <your-repo-url>
cd ubiety-iot-status-service
docker-compose up --build
```

### 2. API Usage
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Example: Create a device status
  ```sh
  curl -X POST -H "X-API-Key: supersecretkey123" -H "Content-Type: application/json" \
    -d '{"device_id": "sensor_1", "timestamp": "2025-01-28T15:55:00Z", "battery_level": 85, "rssi": -60, "online": true}' \
    http://localhost:8000/status
  ```
- Example: Get summary
  ```sh
  curl -H "X-API-Key: supersecretkey123" http://localhost:8000/status/summary | jq .
  ```

### 3. Monitoring & Dashboards
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Login: `admin` / `admin` (change password on first login)
  - Add Prometheus data source: `http://prometheus:9090`
  - Import `grafana-dashboard.json` for a ready-made dashboard

---

## API Endpoints
- `POST   /status`         — Add a device status update
- `GET    /status/summary` — Get summary of all devices
- `GET    /status/recent`  — Get recent online statuses
- `GET    /status/at-risk` — Get at-risk devices
- `GET    /status/{device_id}` — Get latest status for a device
- `GET    /status/{device_id}/history` — Get paginated history
- `GET    /metrics`        — Prometheus metrics
- `GET    /health`         — Health check

All endpoints require the header: `X-API-Key: supersecretkey123`

---

## Example: Add Test Data
You can use the provided Python script to add test data:
```python
import requests
import random
from datetime import datetime, timezone

API_URL = "http://localhost:8000/status"
API_KEY = "supersecretkey123"

for i in range(1, 11):
    payload = {
        "device_id": f"sensor_{i}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "battery_level": random.randint(0, 100),
        "rssi": -random.randint(30, 80),
        "online": random.choice([True, False])
    }
    response = requests.post(
        API_URL,
        json=payload,
        headers={"X-API-Key": API_KEY}
    )
    print(f"Added {payload['device_id']}: {response.status_code} {response.text}")
```

---

## Observability
- **Prometheus metrics**: `heartbeat_count_total`, `online_devices`, `at_risk_devices`, `average_battery`, etc.
- **Grafana dashboard**: Visualize device health, battery, and risk trends in real time.

---

## Project Structure
```
.
├── app/
│   ├── api/endpoints/status.py
│   ├── core/database.py
│   ├── core/security.py
│   ├── main.py
│   ├── metrics.py
│   └── models/
│       ├── database.py
│       ├── schemas.py
├── tests/
├── grafana-dashboard.json
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## License
MIT

---

## Author
Aashik Mathew
