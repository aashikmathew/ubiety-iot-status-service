# Ubiety Entry-Level Backend Engineer Take-Home Assessment

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
- **Docker Compose**: One command to start the app and database
- **Alembic migrations**: Version-controlled database schema
- **Comprehensive tests**: Unit and integration tests for all endpoints and edge cases

---

## 🗂️ File Structure

```
Ubiety-assignment/
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
   git clone <your-repo-url>
   cd Ubiety-assignment
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

---

## 🔑 API Key Authentication

All endpoints require the header:
```
X-API-Key: supersecretkey123
```
(The key is set in `docker-compose.yml` as `API_KEY`. Change it for production use.)

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

```sh
pytest
```

- Unit tests: schema validation, edge cases
- Integration tests: all endpoints, error cases, API key auth

---

## 📝 Notes & Gotchas

- **Route order matters:** `/status/summary` must be declared before `/status/{device_id}` in FastAPI to avoid route conflicts.
- **Migrations:** Always run `alembic upgrade head` after starting the containers for the first time or after changing models.
- **API Key:** Change the `API_KEY` in `docker-compose.yml` for production use.
- **Tests:** Integration tests use the same API key and expect the DB to be up.
- **Error handling:** All endpoints return clear error messages and status codes for invalid input, missing keys, or not found.

---

## 🧩 Dependencies

See `requirements.txt` for all Python dependencies:
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- alembic
- pydantic
- python-dotenv
- pytest (+ plugins)
- httpx
- slowapi

---

## 💡 Project Highlights

- **Production-ready**: Dockerized, tested, and uses best practices for API security and DB migrations.
- **Extensible**: Easily add more endpoints, services, or authentication methods.
- **Well-documented**: Clear structure, sample commands, and test coverage.
- **Professional workflow**: Clean commit history, clear README, and robust error handling.

---

## 👨‍💻 Author

Aashik Mathew

