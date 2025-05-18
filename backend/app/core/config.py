from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # サーバー設定
    PORT: int = 3000  # デフォルト値として残す
    HOST: str = "0.0.0.0"  # デフォルト値として残す
    BACKEND_URL: Optional[str] = None
    FRONTEND_URL: Optional[str] = None
    
    # 管理者認証
    ADMIN_TOKEN: str
    
    # Twitter API設定
    TWITTER_API_URL: str = "https://api.twitter.com/2"  # デフォルト値として残す
    TWITTER_BEARER_TOKEN: str
    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    
    class Config:
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False  # 環境変数名の大文字小文字を区別しない

@lru_cache()
def get_settings() -> Settings:
    return Settings() 