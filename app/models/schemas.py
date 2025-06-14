from pydantic import BaseModel, Field, constr
from datetime import datetime
from typing import List

class DeviceStatusCreate(BaseModel):
    device_id: constr(min_length=1) = Field(..., json_schema_extra={"example": "sensor-abc-123"})
    timestamp: datetime
    battery_level: int = Field(..., ge=0, le=100)
    rssi: int
    online: bool

class DeviceStatusResponse(DeviceStatusCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class HistoricalStatusResponse(BaseModel):
    device_id: str
    statuses: List[DeviceStatusResponse]
    total_records: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True