from fastapi import FastAPI
from app.api.endpoints import status

app = FastAPI()

app.include_router(status.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}