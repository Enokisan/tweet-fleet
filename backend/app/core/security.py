from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from .config import get_settings

API_KEY_NAME = "X-Admin-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    settings = get_settings()
    if api_key_header != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key_header 