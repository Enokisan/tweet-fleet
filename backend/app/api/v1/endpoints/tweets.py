from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ....core.security import verify_token
from ....services.twitter import twitter_service

router = APIRouter()

class TweetCreate(BaseModel):
    text: str

@router.post("/tweets")
async def create_tweet(
    tweet: TweetCreate,
    token: dict = Depends(verify_token)
):
    """
    ツイートを投稿する
    JWT認証が必要
    """
    return await twitter_service.post_tweet(tweet.text) 