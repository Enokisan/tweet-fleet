from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import tweets, auth
from .core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Tweet Fleet API",
    description="Tweet FleetのバックエンドAPI",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL] if settings.FRONTEND_URL else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの追加
app.include_router(tweets.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Tweet Fleet API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)