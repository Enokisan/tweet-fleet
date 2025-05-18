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
    ADMIN_PASSWORD: str
    JWT_SECRET: str
    
    # Twitter API設定
    TWITTER_API_URL: str = "https://api.twitter.com/2"  # デフォルト値として残す
    TWITTER_BEARER_TOKEN: str
    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    
    # GitHub設定
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_REPO: Optional[str] = None
    GITHUB_DIRECTORY_PATH: str = ""
    
    class Config:
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False  # 環境変数名の大文字小文字を区別しない
        env_prefix = ""  # 環境変数のプレフィックスを空に
        env_nested_delimiter = "__"  # ネストされた環境変数の区切り文字
        extra = "ignore"  # 未定義の環境変数は無視

@lru_cache()
def get_settings() -> Settings:
    return Settings() 