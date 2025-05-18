from fastapi import APIRouter, HTTPException
from ....services.twitter import twitter_service
from ....core.config import get_settings

router = APIRouter()
settings = get_settings()

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