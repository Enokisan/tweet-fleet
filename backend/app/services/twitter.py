from typing import Optional, Dict
import tweepy
from ..core.config import get_settings

settings = get_settings()

class TwitterService:
    def __init__(self):
        self.settings = get_settings()
        self._client = None

    @property
    def client(self) -> tweepy.Client:
        """Twitter APIクライアントを取得"""
        if not self._client:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> tweepy.Client:
        """Twitter APIクライアントを作成"""
        try:
            client = tweepy.Client(
                consumer_key=self.settings.TWITTER_API_KEY,
                consumer_secret=self.settings.TWITTER_API_SECRET,
                access_token=self.settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=self.settings.TWITTER_ACCESS_TOKEN_SECRET
            )
            return client
        except Exception as e:
            raise

    async def check_auth(self) -> dict:
        """
        認証状態を確認する
        
        Returns:
            dict: 認証状態
        """
        try:
            # クライアントの作成を試みる
            self._create_client()
            return {
                "success": True,
                "status": "authenticated"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def post_tweet(self, text: str) -> dict:
        """
        ツイートを投稿する
        
        Args:
            text (str): 投稿するテキスト
            
        Returns:
            dict: 投稿結果
        """
        try:
            response = self.client.create_tweet(text=text)
            return {
                "success": True,
                "tweet_id": response.data["id"],
                "text": text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

twitter_service = TwitterService() 