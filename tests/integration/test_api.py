import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)
headers = {"X-API-Key": "supersecretkey123"}

def test_create_and_summary():
    payload = {
        "device_id": "sensor-test-2",
        "timestamp": "2025-06-09T14:00:00Z",
        "battery_level": 90,
        "rssi": -50,
        "online": True
    }
    response = client.post("/status", json=payload, headers=headers)
    assert response.status_code == 201

    response = client.get("/status/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "devices" in data
    assert "total_devices" in data
    assert any(d["device_id"] == "sensor-test-2" for d in data["devices"])

def test_get_nonexistent_device():
    response = client.get("/status/nonexistent-device", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"

def test_summary_with_multiple_devices():
    payload1 = {
        "device_id": "sensor-a",
        "timestamp": "2025-06-09T14:00:00Z",
        "battery_level": 80,
        "rssi": -40,
        "online": True
    }
    payload2 = {
        "device_id": "sensor-b",
        "timestamp": "2025-06-09T15:00:00Z",
        "battery_level": 60,
        "rssi": -70,
        "online": False
    }
    client.post("/status", json=payload1, headers=headers)
    client.post("/status", json=payload2, headers=headers)
    response = client.get("/status/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    ids = [d["device_id"] for d in data["devices"]]
    assert "sensor-a" in ids
    assert "sensor-b" in ids
    assert data["total_devices"] >= 2

def test_historical_status():
    # Create multiple status updates for a device
    device_id = "sensor-hist-test"
    timestamps = [
        (datetime.now() - timedelta(minutes=i)).isoformat()
        for i in range(15)  # Create 15 status updates
    ]
    
    for ts in timestamps:
        payload = {
            "device_id": device_id,
            "timestamp": ts,
            "battery_level": 90,
            "rssi": -50,
            "online": True
        }
        client.post("/status", json=payload, headers=headers)

    # Test default pagination (page 1, size 10)
    response = client.get(f"/status/{device_id}/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == device_id
    assert len(data["statuses"]) == 10  # Default page size
    assert data["total_records"] == 15
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_pages"] == 2

    # Test second page
    response = client.get(f"/status/{device_id}/history?page=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["statuses"]) == 5  # Remaining records
    assert data["page"] == 2

    # Test custom page size
    response = client.get(f"/status/{device_id}/history?page_size=5", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["statuses"]) == 5
    assert data["total_pages"] == 3

    # Test invalid page number
    response = client.get(f"/status/{device_id}/history?page=999", headers=headers)
    assert response.status_code == 400

    # Test nonexistent device
    response = client.get("/status/nonexistent-device/history", headers=headers)
    assert response.status_code == 404

def test_battery_level_out_of_bounds():
    payload = {
        "device_id": "sensor-x",
        "timestamp": "2025-06-14T10:00:00Z",
        "battery_level": 150,  # Invalid
        "rssi": -55,
        "online": True
    }
    response = client.post("/status", json=payload, headers=headers)
    assert response.status_code == 422

def test_missing_api_key():
    payload = {
        "device_id": "sensor-y",
        "timestamp": "2025-06-14T10:00:00Z",
        "battery_level": 90,
        "rssi": -40,
        "online": True
    }
    response = client.post("/status", json=payload)  # No header
    assert response.status_code == 401