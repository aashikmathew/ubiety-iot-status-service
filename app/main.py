"""
Main FastAPI application entrypoint for the Ubiety IoT Device Status Service.
Includes all status endpoints and a health check route.
"""
from fastapi import FastAPI
from app.api.endpoints import status

app = FastAPI()

app.include_router(status.router)

@app.get("/health")
def health_check() -> dict:
    """
    Health check endpoint for container orchestration and uptime monitoring.
    """
    return {"status": "ok"}