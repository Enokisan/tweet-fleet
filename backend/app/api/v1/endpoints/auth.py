from fastapi import APIRouter, HTTPException, Depends
from ....services.twitter import twitter_service
from ....core.config import get_settings
from ....core.security import create_access_token
from pydantic import BaseModel

router = APIRouter()
settings = get_settings()

class PasswordAuth(BaseModel):
    password: str

@router.post("/auth/login")
async def login(auth_data: PasswordAuth):
    """
    パスワード認証を行い、JWTトークンを発行
    """
    if auth_data.password != settings.ADMIN_PASSWORD:
        print("認証失敗: パスワードが一致しません")
        raise HTTPException(
            status_code=401,
            detail="パスワードが正しくありません"
        )
    
    print("認証成功: JWTトークンを発行します")
    access_token = create_access_token()
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/twitter")
async def twitter_auth():
    """
    Twitter認証の状態を確認
    """
    try:
        # 認証状態を確認
        auth_status = await twitter_service.check_auth()
        if auth_status["success"]:
            return {"status": "authenticated"}
        else:
            raise HTTPException(
                status_code=401,
                detail="Twitter認証に失敗しました"
            )
    except Exception as e:
        print(f"Twitter認証エラー: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Twitter認証の確認に失敗しました: {str(e)}"
        ) 