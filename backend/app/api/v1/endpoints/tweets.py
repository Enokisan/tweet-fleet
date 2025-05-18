from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ....core.security import get_api_key
from ....services.twitter import twitter_service

router = APIRouter()

class TweetCreate(BaseModel):
    text: str

@router.post("/tweets")
async def create_tweet(
    tweet: TweetCreate,
    api_key: str = Depends(get_api_key)
):
    """
    ツイートを投稿する
    """
    return await twitter_service.post_tweet(tweet.text) 