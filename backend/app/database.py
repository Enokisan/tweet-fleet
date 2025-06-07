from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from pathlib import Path

# 環境に応じてデータベースURLを決定
def get_database_url():
    # Railway環境でのPostgreSQL
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    # 開発環境でのSQLite
    database_path = Path(__file__).parent.parent / "tweet_fleet.db"
    return f"sqlite:///{database_path}"

def get_async_database_url():
    # Railway環境でのPostgreSQL
    if os.getenv("DATABASE_URL"):
        db_url = os.getenv("DATABASE_URL")
        # PostgreSQLの場合はpsycopg2を使用
        if db_url.startswith("postgresql://"):
            return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url
    
    # 開発環境でのSQLite
    database_path = Path(__file__).parent.parent / "tweet_fleet.db"
    return f"sqlite+aiosqlite:///{database_path}"

DATABASE_URL = get_database_url()
ASYNC_DATABASE_URL = get_async_database_url()

# 同期エンジン（マイグレーション用）
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 非同期エンジン（FastAPI用）
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# データベースセッションの依存性注入
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 