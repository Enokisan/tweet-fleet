from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import get_settings
import jwt
from datetime import datetime, timedelta

settings = get_settings()

# JWT設定
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(hours=1)

security = HTTPBearer()

def create_access_token(data: dict = None) -> str:
    """
    JWTトークンを生成
    """
    expire = datetime.utcnow() + JWT_EXPIRATION_DELTA
    to_encode = {
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": "admin"
    }
    
    if data:
        to_encode.update(data)
    
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    JWTトークンを検証
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="トークンの有効期限が切れています"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="無効なトークンです"
        ) 