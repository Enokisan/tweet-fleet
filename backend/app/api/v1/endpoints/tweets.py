from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ....core.security import verify_token
from ....services.twitter import twitter_service
from ....services.twitter_oauth import TwitterOAuthService
from ....database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
twitter_oauth_service = TwitterOAuthService()

class TweetCreate(BaseModel):
    text: str

@router.post("/tweets")
async def create_tweet(
    tweet: TweetCreate,
    token: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """
    ツイートを投稿する
    JWT認証が必要
    """
    try:
        # JWTトークンからユーザーIDを取得
        user_id = token.get("sub")
        if not user_id or user_id == "admin":
            # 従来の管理者認証の場合は既存のアクセストークンを使用
            return await twitter_service.post_tweet(tweet.text)
        
        # ユーザーのTwitterトークンを取得
        oauth_token = await twitter_oauth_service.get_user_twitter_token(db, int(user_id))
        if not oauth_token:
            raise HTTPException(
                status_code=401,
                detail="Twitter認証が必要です。先にTwitter認証を行ってください。"
            )
        
        if oauth_token.is_expired():
            raise HTTPException(
                status_code=401,
                detail="Twitterトークンが期限切れです。再認証が必要です。"
            )
        
        # OAuth 2.0トークンを使用してツイート投稿
        return await twitter_service.post_tweet(tweet.text, oauth_token.access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ツイート投稿に失敗しました: {str(e)}"
        ) 