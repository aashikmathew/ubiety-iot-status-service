# Ubiety IoT Device Status Service

## Overview
A REST API service for managing IoT device status updates from Ubiety's network of smart home sensors. The service receives, validates, stores, and serves device status data including device ID, timestamp, battery level, signal strength (RSSI), and online status.

## 🏗️ Architecture & Design Decisions

### Technology Stack
- **Framework**: FastAPI (Python) - Fast, modern, with automatic OpenAPI documentation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Testing**: Pytest with pytest-asyncio
- **Authentication**: API Key-based (Bonus feature)
- **Deployment**: Docker & Docker Compose
- **Data Validation**: Pydantic models

### Database Schema
```sql
-- Device status table (stores historical data for bonus feature)
CREATE TABLE device_status (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    battery_level INTEGER NOT NULL CHECK (battery_level >= 0 AND battery_level <= 100),
    rssi INTEGER NOT NULL,
    online BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    INDEX idx_device_timestamp (device_id, timestamp DESC)
);

-- API keys table (bonus feature)
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key_name VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## ⚙️ Configuration Management

### Environment Variables
Create a `.env` file based on `.env.example`:

```bash
# Database Configuration
DATABASE_URL=postgresql://ubiety:password@localhost:5432/ubiety_iot
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# Authentication (Optional)
API_KEY_HEADER=X-API-Key
ENABLE_AUTH=false

# Application Settings
APP_NAME=Ubiety IoT Status Service
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# Security
CORS_ORIGINS=["http://localhost:3000"]
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Performance
REDIS_URL=redis://localhost:6379/0  # For caching
MAX_WORKERS=4
```

### Required vs Optional Variables
- **Required**: `DATABASE_URL`
- **Optional**: All others have sensible defaults

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL (or use Docker setup)

### Option 1: Docker Setup (Recommended)
```bash
# Clone and setup
git clone <your-repo>
cd ubiety-iot-service

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# The API will be available at http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 API Endpoints

### 1. POST /status
Submit device status update.

**Headers** (Bonus - if authentication enabled):
```
X-API-Key: your-api-key-here
```

**Request Body**:
```json
{
    "device_id": "sensor-abc-123",
    "timestamp": "2025-06-09T14:00:00Z",
    "battery_level": 76,
    "rssi": -60,
    "online": true
}
```

**Successful Response (200)**:
```json
{
    "status": "success",
    "message": "Device status updated successfully",
    "device_id": "sensor-abc-123"
}
```

**Error Responses**:
```json
// 400 Bad Request - Invalid payload
{
    "detail": [
        {
            "loc": ["body", "battery_level"],
            "msg": "ensure this value is less than or equal to 100",
            "type": "value_error.number.not_le",
            "ctx": {"limit_value": 100}
        }
    ]
}

// 401 Unauthorized - Invalid API key
{
    "detail": "Invalid API key"
}

// 422 Unprocessable Entity - Missing required fields
{
    "detail": [
        {
            "loc": ["body", "device_id"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### 2. GET /status/{device_id}
Get the latest status for a specific device.

**Successful Response (200)**:
```json
{
    "device_id": "sensor-abc-123",
    "timestamp": "2025-06-09T14:00:00Z",
    "battery_level": 76,
    "rssi": -60,
    "online": true,
    "last_updated": "2025-06-09T14:00:05Z"
}
```

**Error Responses**:
```json
// 404 Not Found - Device not found
{
    "detail": "Device sensor-xyz-999 not found"
}

// 401 Unauthorized - Invalid API key (if auth enabled)
{
    "detail": "Invalid API key"
}
```

### 3. GET /status/summary
Get summary of all devices with their latest status.

**Successful Response (200)**:
```json
{
    "devices": [
        {
            "device_id": "sensor-abc-123",
            "battery_level": 76,
            "online": true,
            "last_update": "2025-06-09T14:00:00Z"
        },
        {
            "device_id": "sensor-xyz-456",
            "battery_level": 45,
            "online": false,
            "last_update": "2025-06-09T13:30:00Z"
        }
    ],
    "total_devices": 2,
    "online_devices": 1,
    "offline_devices": 1
}
```

### 4. GET /status/{device_id}/history (Bonus)
Get historical status updates for a device.

**Query Parameters**:
- `limit`: Number of records (default: 50, max: 1000)
- `since`: ISO timestamp to filter records after this time

**Successful Response (200)**:
```json
{
    "device_id": "sensor-abc-123",
    "history": [
        {
            "timestamp": "2025-06-09T14:00:00Z",
            "battery_level": 76,
            "rssi": -60,
            "online": true
        },
        {
            "timestamp": "2025-06-09T13:30:00Z",
            "battery_level": 78,
            "rssi": -58,
            "online": true
        }
    ],
    "total_records": 2,
    "has_more": false
}
```

### 5. GET /health (System Health Check)
Health check endpoint for monitoring.

**Response (200)**:
```json
{
    "status": "healthy",
    "timestamp": "2025-06-09T14:00:00Z",
    "database": "connected",
    "version": "1.0.0"
}
```

## 🔒 Security Hardening

### CORS Configuration
```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Configure for your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Security Headers
```python
# app/middleware/security.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
```

### Rate Limiting
```python
# app/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Usage in endpoints
@app.post("/status")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def submit_status(request: Request, ...):
    # endpoint logic
```

## 📊 Performance Benchmarks

### Expected Performance
- **Throughput**: 1000+ requests/second on standard hardware
- **Latency**: <100ms p95 for all endpoints
- **Database**: <50ms query response time
- **Memory**: <512MB RAM usage under normal load

### Load Testing
```bash
# Install load testing tool
pip install locust

# Run load test
locust -f tests/load_test.py --host http://localhost:8000

# Alternative with wrk
wrk -t12 -c400 -d30s --script=tests/load_test.lua http://localhost:8000/status/summary
```

### Example Load Test (locust)
```python
# tests/load_test.py
from locust import HttpUser, task, between

class IoTDeviceUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_summary(self):
        self.client.get("/status/summary")
    
    @task(2)
    def get_device_status(self):
        self.client.get("/status/sensor-abc-123")
    
    @task(1)
    def submit_status(self):
        self.client.post("/status", json={
            "device_id": "sensor-load-test",
            "timestamp": "2025-06-09T14:00:00Z",
            "battery_level": 85,
            "rssi": -65,
            "online": True
        })
```

## 🔄 Data Migration Strategy

### Alembic Migration Management
```bash
# Create new migration
alembic revision --autogenerate -m "Add new field to device_status"

# Review generated migration
# Edit alembic/versions/xxx_add_new_field.py if needed

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Schema Evolution Examples
```python
# alembic/versions/002_add_location_field.py
def upgrade():
    op.add_column('device_status', 
        sa.Column('location', sa.String(255), nullable=True))
    
    # Backfill existing records
    op.execute("UPDATE device_status SET location = 'unknown' WHERE location IS NULL")
    
    # Make non-nullable after backfill
    op.alter_column('device_status', 'location', nullable=False)

def downgrade():
    op.drop_column('device_status', 'location')
```

### Migration Best Practices
1. **Test migrations** on staging data first
2. **Backup database** before major schema changes
3. **Use transactions** for complex migrations
4. **Monitor performance** impact of migrations
5. **Plan rollback strategy** for each migration

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# All tests with coverage
pytest --cov=app tests/ --cov-report=html

# Load tests
locust -f tests/load_test.py --headless -u 100 -r 10 -t 30s --host http://localhost:8000
```

### Test Structure
```
tests/
├── unit/
│   ├── test_models.py          # Test Pydantic models & validation
│   ├── test_database.py        # Test database operations
│   ├── test_health_logic.py    # Test device health rules
│   └── test_auth.py            # Test authentication (bonus)
├── integration/
│   ├── test_api_endpoints.py   # Test complete API workflows
│   ├── test_database_integration.py
│   └── test_auth_integration.py
├── load_test.py                # Performance testing
└── conftest.py                 # Pytest fixtures
```

### Key Test Cases
- **Health Rules**: Battery level validation (0-100), RSSI validation
- **Data Validation**: Invalid JSON, missing fields, wrong data types
- **Database Operations**: CRUD operations, constraint violations
- **API Integration**: Full request/response cycles
- **Authentication**: Valid/invalid API keys (bonus)
- **Edge Cases**: Duplicate timestamps, device not found
- **Error Handling**: All 4xx/5xx response scenarios
- **Performance**: Load testing under various conditions

## 🔧 Implementation Blueprint

### Phase 1: Core API (90 minutes)
1. **Setup Project Structure** (15 min)
   - Initialize FastAPI project
   - Setup database models with SQLAlchemy
   - Create Pydantic schemas for validation

2. **Database Layer** (20 min)
   - Design and implement database models
   - Setup Alembic for migrations
   - Create database connection management

3. **API Endpoints** (30 min)
   - POST /status with validation
   - GET /status/{device_id}
   - GET /status/summary with aggregation

4. **Business Logic** (15 min)
   - Device health validation rules
   - Data sanitization and validation
   - Error handling and logging

5. **Documentation** (10 min)
   - OpenAPI/Swagger documentation
   - Response models and examples

### Phase 2: Testing (30-60 minutes)
1. **Unit Tests** (30 min)
   - Test models and validation logic
   - Test database operations
   - Test health rules and edge cases

2. **Integration Tests** (30 min)
   - Test complete API workflows
   - Test database integration
   - Test error handling

### Phase 3: Bonus Features (Optional)
1. **Authentication** (30 min)
   - API key-based authentication
   - Middleware for request validation
   - API key management

2. **Docker Setup** (20 min)
   - Dockerfile for the application
   - Docker Compose with PostgreSQL
   - Environment configuration

3. **Historical Data** (40 min)
   - Modify schema to store all updates
   - Add history endpoint
   - Implement pagination and filtering

## 🐳 Docker Configuration

### docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://ubiety:password@db:5432/ubiety_iot
      - API_KEY_HEADER=X-API-Key
    depends_on:
      - db
    volumes:
      - ./app:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=ubiety
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ubiety_iot
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=app tests/ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 🎯 Alternative Implementation Approaches

### 1. **Flask + SQLAlchemy** (Traditional)
- **Pros**: Mature ecosystem, extensive documentation
- **Cons**: More boilerplate, manual OpenAPI setup
- **Best for**: Teams familiar with Flask, legacy integration

### 2. **Django REST Framework**
- **Pros**: Built-in admin, ORM, authentication
- **Cons**: Heavier framework, more complex for simple APIs
- **Best for**: Larger applications, teams familiar with Django

### 3. **Node.js + Express + TypeScript**
- **Pros**: JavaScript ecosystem, fast development
- **Cons**: Different from Python requirement
- **Best for**: Full-stack JavaScript teams

### 4. **Go + Gin/Echo**
- **Pros**: High performance, compiled binary
- **Cons**: More verbose, smaller ecosystem
- **Best for**: Performance-critical applications

### 5. **Serverless (AWS Lambda + API Gateway)**
- **Pros**: Auto-scaling, pay-per-use
- **Cons**: Cold starts, vendor lock-in
- **Best for**: Variable load, cost optimization

## 📈 Performance Considerations

### Database Optimization
- Index on `(device_id, timestamp DESC)` for fast latest status queries
- Consider partitioning by time for historical data
- Connection pooling for concurrent requests

### Caching Strategy
- Redis for frequently accessed device status
- Cache summary endpoint results
- Implement cache invalidation on updates

### Monitoring & Observability
- Health check endpoint: `GET /health`
- Metrics collection (Prometheus)
- Structured logging with correlation IDs
- Distributed tracing for debugging

## 📦 Project Structure
```
ubiety-iot-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLAlchemy models
│   │   └── schemas.py          # Pydantic models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Auth and DB dependencies
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       └── status.py       # Status endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # DB connection
│   │   └── security.py         # Authentication logic
│   ├── services/
│   │   ├── __init__.py
│   │   └── device_service.py   # Business logic
│   └── middleware/
│       ├── __init__.py
│       ├── security.py         # Security headers
│       └── rate_limit.py       # Rate limiting
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── load_test.py
│   └── conftest.py
├── alembic/                    # Database migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── alembic.ini
└── README.md
```

This blueprint provides a production-ready implementation with comprehensive testing, bonus features, and multiple deployment options. The modular structure allows for easy maintenance and extension. 