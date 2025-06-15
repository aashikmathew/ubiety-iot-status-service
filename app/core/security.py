import os
from fastapi import Header, HTTPException, status

# API key value and header name (set via environment or default for local/dev)
API_KEY = os.getenv("API_KEY", "supersecretkey123")
API_KEY_NAME = "X-API-Key"

def get_api_key(x_api_key: str | None = Header(None, alias="X-API-Key")) -> str:
    """
    Dependency to enforce API key authentication on endpoints.
    Raises 401 if the key is missing or invalid.
    """
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Unauthorized", "message": "Invalid or missing API key"}
        )
    return x_api_key