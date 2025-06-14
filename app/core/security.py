import os
from fastapi import Header, HTTPException, status, Depends

# API key value and header name (set via environment or default for local/dev)
API_KEY = os.getenv("API_KEY", "supersecretkey123")
API_KEY_NAME = "X-API-Key"

def get_api_key(x_api_key: str = Header(...)) -> str:
    """
    Dependency to enforce API key authentication on endpoints.
    Raises 401 if the key is missing or invalid.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return x_api_key