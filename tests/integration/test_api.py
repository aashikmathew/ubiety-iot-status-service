import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_summary():
    payload = {
        "device_id": "sensor-test-2",
        "timestamp": "2025-06-09T14:00:00Z",
        "battery_level": 90,
        "rssi": -50,
        "online": True
    }
    response = client.post("/status", json=payload)
    assert response.status_code == 201

    response = client.get("/status/summary")
    assert response.status_code == 200
    data = response.json()
    assert "devices" in data
    assert "total_devices" in data
    assert any(d["device_id"] == "sensor-test-2" for d in data["devices"])

def test_get_nonexistent_device():
    response = client.get("/status/nonexistent-device")
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
    client.post("/status", json=payload1)
    client.post("/status", json=payload2)
    response = client.get("/status/summary")
    assert response.status_code == 200
    data = response.json()
    ids = [d["device_id"] for d in data["devices"]]
    assert "sensor-a" in ids
    assert "sensor-b" in ids
    assert data["total_devices"] >= 2