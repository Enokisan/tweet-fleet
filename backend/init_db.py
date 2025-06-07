#!/usr/bin/env python3
"""
データベースを初期化するスクリプト
"""
import asyncio
from app.database import engine, Base
from app.models import User, OAuthToken

async def init_database():
    """データベースとテーブルを作成"""
    print("データベースを初期化しています...")
    
    # テーブルを作成
    Base.metadata.create_all(bind=engine)
    
    print("データベースの初期化が完了しました！")
    print(f"データベースファイル: {engine.url}")

if __name__ == "__main__":
    asyncio.run(init_database()) 