from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DeviceStatus(Base):
    """
    SQLAlchemy model for storing IoT device status updates.
    Each row represents a single status update for a device.
    """
    __tablename__ = "device_status"

    id = Column(Integer, primary_key=True, index=True)  # Unique status record ID
    device_id = Column(String(255), nullable=False, index=True)  # Device identifier
    timestamp = Column(DateTime(timezone=True), nullable=False)  # When the status was recorded
    battery_level = Column(Integer, nullable=False)  # Battery percentage (0-100)
    rssi = Column(Integer, nullable=False)  # Signal strength
    online = Column(Boolean, nullable=False)  # Device online status
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Record creation time