from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.database import DeviceStatus
from app.models.schemas import DeviceStatusCreate, DeviceStatusResponse, HistoricalStatusResponse
from app.core.security import get_api_key
from typing import Optional
from math import ceil


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

@router.get("/status/{device_id}/history", response_model=HistoricalStatusResponse)
def get_historical_status(
    device_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    # Check if device exists
    device_exists = db.query(DeviceStatus).filter(DeviceStatus.device_id == device_id).first()
    if not device_exists:
        raise HTTPException(status_code=404, detail="Device not found")

    # Get total count of records
    total_records = db.query(DeviceStatus).filter(DeviceStatus.device_id == device_id).count()
    
    # Calculate pagination
    total_pages = ceil(total_records / page_size)
    if page > total_pages and total_pages > 0:
        raise HTTPException(status_code=400, detail=f"Page number exceeds total pages ({total_pages})")

    # Get paginated results
    statuses = (
        db.query(DeviceStatus)
        .filter(DeviceStatus.device_id == device_id)
        .order_by(DeviceStatus.timestamp.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "device_id": device_id,
        "statuses": statuses,
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

