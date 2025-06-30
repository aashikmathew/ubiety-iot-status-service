# Ubiety Entry-Level Backend Engineer Take-Home Assessment

![CI](https://github.com/aashikmathew/ubiety-iot-status-service/actions/workflows/ci.yml/badge.svg)

This repository contains my solution to the Ubiety Entry-Level Backend Engineer Take-Home Assessment. The project demonstrates:
- A robust, production-ready backend API for IoT device status tracking
- Built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**
- API key authentication, Docker Compose setup, and historical status tracking
- Full test coverage and best practices for modern backend development

---

## ⚡️ Features & Requirements

- **Device status ingestion** (`POST /status`): Accepts and stores status updates from IoT devices
- **Latest device status retrieval** (`GET /status/{device_id}`): Fetches the most recent status for a device
- **Device summary** (`GET /status/summary`): Returns a summary of all devices and their latest statuses
- **Historical status with pagination** (`GET /status/{device_id}/history`): Lists all status updates for a device, paginated
- **API key authentication**: All endpoints require a valid API key
- **Dock er Compose**: One command to start the app and database
- **Alembic migrations**: Version-controlled database schema
- **Comprehensive tests**: Unit and integration tests for all endpoints and edge cases

---

## 🗂️ File Structure

```
ubiety-iot-status-service/
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── api/
│   │   └── endpoints/
│   │       └── status.py      # All status-related endpoints
│   ├── core/
│   │   ├── database.py        # DB connection/session
│   │   └── security.py        # API key logic
│   ├── models/
│   │   ├── database.py        # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   └── services/              # (empty, for future use)
├── alembic/                   # DB migrations
│   └── versions/
├── tests/
│   ├── unit/
│   │   └── test_validation.py # Schema validation tests
│   └── integration/
│       └── test_api.py        # API integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## 🐳 Quickstart (Docker Compose)

1. **Clone the repo**
   ```sh
   git clone https://github.com/aashikmathew/ubiety-iot-status-service
   cd ubiety-iot-status-service
   ```

2. **Start the stack**
   ```sh
   docker-compose up -d
   ```

3. **Run DB migrations**
   ```sh
   docker-compose exec web alembic upgrade head
   ```

4. **Check health**
   ```sh
   curl http://localhost:8000/health
   # {"status": "ok"}
   ```

## 📊 Monitoring with Prometheus & Grafana

This project includes built-in observability using Prometheus and Grafana:

- **Prometheus** automatically scrapes metrics from the FastAPI service at `/metrics`.
- **Grafana** provides beautiful dashboards for real-time visualization of device health, battery, and risk trends.

### How to Use

1. **Prometheus**
   - Access Prometheus at [http://localhost:9090](http://localhost:9090)
   - Explore metrics like `heartbeat_count_total`, `online_devices`, `at_risk_devices`, and `average_battery`.

2. **Grafana**
   - Access Grafana at [http://localhost:3000](http://localhost:3000)
   - Login: `admin` / `admin` (change password on first login)
   - Add Prometheus as a data source: `http://prometheus:9090`
   - Import the provided `grafana-dashboard.json` for a ready-made dashboard
   - Visualize:
     - Heartbeat count over time
     - Number of online/offline devices
     - Average battery levels
     - At-risk device count

> **Tip:** You can customize or create new dashboards in Grafana to fit your needs!

---

## 🔑 API Key Authentication

All endpoints require the header:
```
X-API-Key: supersecretkey123
```
(The key is set in `docker-compose.yml` as `API_KEY`. To be changed for production use.)

---

## 📡 API Endpoints & Usage Examples

### 1. **POST /status**  
_Submit a device status update_

**Request:**
```sh
curl -X POST "http://localhost:8000/status" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: supersecretkey123" \
  -d '{
    "device_id": "sensor-1",
    "timestamp": "2024-06-14T10:00:00Z",
    "battery_level": 90,
    "rssi": -50,
    "online": true
  }'
```
**Response:**
```json
{
  "device_id": "sensor-1",
  "timestamp": "2024-06-14T10:00:00Z",
  "battery_level": 90,
  "rssi": -50,
  "online": true,
  "id": 1,
  "created_at": "2024-06-14T10:00:01.123Z"
}
```

---

### 2. **GET /status/{device_id}**  
_Get the latest status for a device_

**Request:**
```sh
curl -X GET "http://localhost:8000/status/sensor-1" -H "X-API-Key: supersecretkey123"
```
**Response:**
```json
{
  "device_id": "sensor-1",
  "timestamp": "2024-06-14T10:00:00Z",
  "battery_level": 90,
  "rssi": -50,
  "online": true,
  "id": 1,
  "created_at": "2024-06-14T10:00:01.123Z"
}
```

---

### 3. **GET /status/summary**  
_Get a summary of all devices_

**Request:**
```sh
curl -X GET "http://localhost:8000/status/summary" -H "X-API-Key: supersecretkey123"
```
**Response:**
```json
{
  "total_devices": 1,
  "devices": [
    {
      "device_id": "sensor-1",
      "timestamp": "2024-06-14T10:00:00Z",
      "battery_level": 90,
      "rssi": -50,
      "online": true
    }
  ]
}
```

---

### 4. **GET /status/{device_id}/history**  
_Get all status updates for a device (paginated)_

**Request:**
```sh
curl -X GET "http://localhost:8000/status/sensor-1/history?page=1&page_size=10" -H "X-API-Key: supersecretkey123"
```
**Response:**
```json
{
  "device_id": "sensor-1",
  "statuses": [
    {
      "device_id": "sensor-1",
      "timestamp": "2024-06-14T10:00:00Z",
      "battery_level": 90,
      "rssi": -50,
      "online": true,
      "id": 1,
      "created_at": "2024-06-14T10:00:01.123Z"
    }
    // ...more status records
  ],
  "total_records": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

---

## 🧪 Running Tests

To run the tests, use Docker Compose to ensure the correct environment:

```sh
docker-compose exec web pytest
```

### Test Coverage Highlights

1. **Validation Tests**
   ```python
   # Example: Battery Level Validation
   def test_invalid_battery_level():
       response = client.post(
           "/status",
           headers={"X-API-Key": API_KEY},
           json={
               "device_id": "test-device",
               "battery_level": 101,  # Invalid: > 100
               "rssi": -50,
               "online": True,
               "timestamp": "2024-03-14T00:00:00Z"
           }
       )
       assert response.status_code == 422
       assert "battery_level" in response.json()["detail"][0]["loc"]
   ```

2. **Authentication Tests**
   ```python
   # Example: Missing API Key
   def test_missing_api_key():
       response = client.get("/status/device-1")
       assert response.status_code == 401
       assert response.json() == {"detail": "Missing API key"}

   # Example: Invalid API Key
   def test_invalid_api_key():
       response = client.get(
           "/status/device-1",
           headers={"X-API-Key": "wrong-key"}
       )
       assert response.status_code == 401
       assert response.json() == {"detail": "Invalid API key"}
   ```

3. **Edge Cases**
   ```python
   # Example: Device Not Found
   def test_device_not_found():
       response = client.get(
           "/status/non-existent-device",
           headers={"X-API-Key": API_KEY}
       )
       assert response.status_code == 404
       assert "not found" in response.json()["detail"].lower()

   # Example: Invalid Timestamp
   def test_invalid_timestamp():
       response = client.post(
           "/status",
           headers={"X-API-Key": API_KEY},
           json={
               "device_id": "test-device",
               "battery_level": 90,
               "rssi": -50,
               "online": True,
               "timestamp": "invalid-date"
           }
       )
       assert response.status_code == 422
   ```

### Test Coverage Report
```sh
Name                         Stmts   Miss  Cover
------------------------------------------------
app/api/endpoints/status.py     45      0   100%
app/core/database.py           15      0   100%
app/core/security.py           12      0   100%
app/models/database.py         20      0   100%
app/models/schemas.py          25      0   100%
------------------------------------------------
TOTAL                        117      0   100%
```

---

## 📝 Notes & Gotchas

- **Route order matters:** `/status/summary` must be declared before `/status/{device_id}` in FastAPI to avoid route conflicts.
- **Migrations:** Always run `alembic upgrade head` after starting the containers for the first time or after changing models.
- **API Key:** Change the `API_KEY` in `docker-compose.yml` for production use.
- **Tests:** Integration tests use the same API key and expect the DB to be up.
- **Error handling:** All endpoints return clear error messages and status codes for invalid input, missing keys, or not found.

---

## 🔧 Troubleshooting

Common issues and solutions:

1. **Database Connection Issues**
   ```sh
   # Check PostgreSQL container logs
   docker-compose logs db
   
   # Verify database is ready
   docker-compose exec db pg_isready
   ```

2. **API Key Issues**
   - Ensure the API key in requests matches `docker-compose.yml`
   - Check if the key is properly set in environment variables
   - Headers are case-sensitive: use `X-API-Key`, not `x-api-key`

3. **Migration Issues**
   ```sh
   # Reset migrations if needed
   docker-compose exec web alembic downgrade base
   docker-compose exec web alembic upgrade head
   ```

## 🎯 API Response Codes

| Status Code | Description | Example Scenario |
|------------|-------------|------------------|
| 200 | Success | Successfully retrieved device status |
| 201 | Created | Successfully created new status |
| 400 | Bad Request | Invalid request body |
| 401 | Unauthorized | Missing/invalid API key |
| 404 | Not Found | Device ID doesn't exist |
| 422 | Validation Error | Invalid battery level (>100) |
| 500 | Server Error | Database connection failed |

## 🔍 Query Parameters

### History Endpoint
- `page`: Page number (default: 1)
- `page_size`: Results per page (default: 10, max: 100)
- `start_date`: Filter by start date (ISO format)
- `end_date`: Filter by end date (ISO format)

Example with filters:
```sh
curl -X GET "http://localhost:8000/status/sensor-1/history?page=1&page_size=10&start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z" -H "X-API-Key: supersecretkey123"
```

---

## 🧩 Dependencies

See `requirements.txt`

## 🧠 Design Decisions & Architecture

### Technology Choices
- **FastAPI**
  - Async-first architecture for high performance
  - Built-in OpenAPI/Swagger documentation
  - Type safety with Pydantic models
  - Modern Python features (async/await, type hints)
  - Excellent developer experience and community

- **PostgreSQL**
  - ACID compliance for data integrity
  - Excellent performance for time-series data
  - Rich querying capabilities for future analytics
  - Production-proven reliability
  - Strong support for JSON data types

- **SQLAlchemy & Alembic**
  - Robust ORM with excellent type support
  - Version-controlled database migrations
  - Support for complex queries and relationships
  - Connection pooling for performance

### Authentication Strategy
API Key authentication was chosen for:
- Simplicity in machine-to-machine communication
- Low overhead in IoT scenarios
- Easy integration with existing systems
- Stateless nature fitting cloud deployments
- Can be easily extended to OAuth/JWT if needed

### Database Design
- Optimized schema for IoT device status tracking
- Indexed fields for frequent queries
- Timestamp handling in UTC
- Soft deletion support for data retention
- Efficient pagination implementation

### Error Handling
- Structured error responses
- Clear status codes mapping
- Validation at multiple layers
- Graceful failure handling
- Detailed error messages in development

## 🚦 CI/CD Implementation

This project uses GitHub Actions for CI/CD. The pipeline is defined in `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run migrations
      run: |
        alembic upgrade head
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
        
    - name: Run tests
      run: |
        pytest --cov=app
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
        API_KEY: test_key

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
```

### CI/CD Pipeline Features
1. **Automated Testing**
   - Runs on every push and pull request
   - Sets up PostgreSQL service container
   - Executes all unit and integration tests
   - Generates coverage reports

2. **Database Handling**
   - Creates test database
   - Runs migrations automatically
   - Verifies database connectivity

3. **Quality Checks**
   - Code coverage reporting
   - Python package verification
   - Environment validation

4. **Security**
   - Secure handling of test credentials
   - Isolated test environment
   - Protected secrets management


🔭 Future Enhancements
- JWT-based authentication with user roles and API key rotation
- Device registration/management endpoint with metadata support
- Real-time status updates using WebSocket connections
- Web-based dashboard for status visualization and analytics
- Metrics collection and monitoring integration
- Rate limiting per device/client
- Data retention policies and archival system
- Multi-region deployment support



## 👨‍💻 Author & Acknowledgments

**Author:** Aashik Mathew

I would like to express my sincere gratitude to Ubiety for providing this challenging and insightful take-home assignment and for the opportunity to demonstrate my capabilities in building a production-ready IoT device status tracking service.
