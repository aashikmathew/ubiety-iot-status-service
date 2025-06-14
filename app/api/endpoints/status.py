from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.database import DeviceStatus
from app.models.schemas import DeviceStatusCreate, DeviceStatusResponse
from app.core.security import get_api_key


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/status", response_model=DeviceStatusResponse, status_code=201)
def create_status(payload: DeviceStatusCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    status_obj = DeviceStatus(**payload.model_dump())
    db.add(status_obj)
    db.commit()
    db.refresh(status_obj)
    return status_obj

@router.get("/status/summary")
def get_status_summary(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    subq = (
        db.query(
            DeviceStatus.device_id,
            DeviceStatus.battery_level,
            DeviceStatus.online,
            DeviceStatus.timestamp
        )
        .distinct(DeviceStatus.device_id)
        .order_by(DeviceStatus.device_id, DeviceStatus.timestamp.desc())
        .all()
    )
    devices = [
        {
            "device_id": row.device_id,
            "battery_level": row.battery_level,
            "online": row.online,
            "last_update": row.timestamp
        }
        for row in subq
    ]
    return {
        "devices": devices,
        "total_devices": len(devices),
        "online_devices": sum(1 for d in devices if d["online"]),
        "offline_devices": sum(1 for d in devices if not d["online"])
    }

@router.get("/status/{device_id}", response_model=DeviceStatusResponse)
def get_latest_status(device_id: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    status_obj = (
        db.query(DeviceStatus)
        .filter(DeviceStatus.device_id == device_id)
        .order_by(DeviceStatus.timestamp.desc())
        .first()
    )
    if not status_obj:
        raise HTTPException(status_code=404, detail="Device not found")
    return status_obj

