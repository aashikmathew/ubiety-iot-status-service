import pytest
from app.models.schemas import DeviceStatusCreate
from pydantic import ValidationError

def test_battery_level_out_of_range():
    # Battery level too high
    with pytest.raises(ValidationError):
        DeviceStatusCreate(
            device_id="sensor-1",
            timestamp="2025-06-09T14:00:00Z",
            battery_level=150,  # Invalid
            rssi=-60,
            online=True
        )
    # Battery level too low
    with pytest.raises(ValidationError):
        DeviceStatusCreate(
            device_id="sensor-1",
            timestamp="2025-06-09T14:00:00Z",
            battery_level=-10,  # Invalid
            rssi=-60,
            online=True
        )

def test_missing_required_fields():
    with pytest.raises(ValidationError):
        DeviceStatusCreate(
            timestamp="2025-06-09T14:00:00Z",
            battery_level=50,
            rssi=-60,
            online=True
        )  # Missing device_id

def test_valid_payload():
    # Should not raise
    DeviceStatusCreate(
        device_id="sensor-1",
        timestamp="2025-06-09T14:00:00Z",
        battery_level=50,
        rssi=-60,
        online=True
    )


def test_invalid_type_for_battery_level():
    with pytest.raises(ValidationError):
        DeviceStatusCreate(
            device_id="sensor-1",
            timestamp="2025-06-09T14:00:00Z",
            battery_level="not-an-int",  # Invalid type
            rssi=-60,
            online=True
        )

def test_empty_device_id():
    with pytest.raises(ValidationError):
        DeviceStatusCreate(
            device_id="",
            timestamp="2025-06-09T14:00:00Z",
            battery_level=50,
            rssi=-60,
            online=True
        )

