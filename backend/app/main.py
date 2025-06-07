from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import tweets, auth, github
from .core.config import get_settings
from .database import Base, engine

settings = get_settings()

app = FastAPI(
    title="Tweet Fleet API",
    description="Tweet FleetのバックエンドAPI",
    version="0.1.0"
)

# データベースの初期化
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    print("アプリケーションを開始しています...")
    
    # データベーステーブルを作成（存在しない場合のみ）
    from .database import engine, Base
    from .models import User, OAuthToken  # モデルをインポートして確実に登録
    
    try:
        print("データベーステーブルを確認中...")
        Base.metadata.create_all(bind=engine)
        print("データベーステーブルの確認が完了しました")
    except Exception as e:
        print(f"データベース初期化エラー: {e}")
        # エラーがあっても起動は継続

# CORS設定
allowed_origins = [
    "http://localhost:5173",  # Viteのデフォルトポート
    "http://localhost:5174",  # Viteの代替ポート
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

# 設定ファイルからフロントエンドURLが指定されている場合は追加
if settings.FRONTEND_URL:
    allowed_origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ルーターの追加
app.include_router(tweets.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(github.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Tweet Fleet API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)