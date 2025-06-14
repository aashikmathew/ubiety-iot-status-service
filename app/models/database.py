from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DeviceStatus(Base):
    __tablename__ = "device_status"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(255), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    battery_level = Column(Integer, nullable=False)
    rssi = Column(Integer, nullable=False)
    online = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())