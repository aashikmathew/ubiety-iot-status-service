from pydantic import BaseModel, Field, constr
from datetime import datetime
from typing import List

class DeviceStatusCreate(BaseModel):
    """
    Schema for creating a new device status update (request body).
    """
    device_id: constr(min_length=1) = Field(..., json_schema_extra={"example": "sensor-abc-123"})
    timestamp: datetime  # ISO8601 timestamp of the status
    battery_level: int = Field(..., ge=0, le=100)  # Battery percentage (0-100)
    rssi: int  # Signal strength
    online: bool  # Device online status

class DeviceStatusResponse(DeviceStatusCreate):
    """
    Schema for returning a device status update (response body).
    Includes DB-generated fields.
    """
    id: int  # Unique status record ID
    created_at: datetime  # Record creation time

    class Config:
        from_attributes = True

class HistoricalStatusResponse(BaseModel):
    """
    Schema for paginated historical status response for a device.
    """
    device_id: str
    statuses: List[DeviceStatusResponse]
    total_records: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True