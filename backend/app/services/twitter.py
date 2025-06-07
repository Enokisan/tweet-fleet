from typing import Optional, Dict
import tweepy
from ..core.config import get_settings
from ..models.oauth_token import OAuthToken
from sqlalchemy.ext.asyncio import AsyncSession

settings = get_settings()

class TwitterService:
    def __init__(self):
        self.settings = get_settings()
        self._client = None

    @property
    def client(self) -> tweepy.Client:
        """Twitter APIクライアントを取得（従来のアクセストークン用）"""
        if not self._client:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> tweepy.Client:
        """Twitter APIクライアントを作成（従来のアクセストークン用）"""
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

    def create_oauth_client(self, access_token: str) -> tweepy.Client:
        """OAuth 2.0トークンを使用してTwitter APIクライアントを作成"""
        try:
            client = tweepy.Client(bearer_token=access_token)
            return client
        except Exception as e:
            raise Exception(f"OAuthクライアント作成に失敗: {str(e)}")

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

    async def post_tweet(self, text: str, access_token: Optional[str] = None) -> dict:
        """
        ツイートを投稿する
        
        Args:
            text (str): 投稿するテキスト
            access_token (str, optional): OAuth 2.0アクセストークン
            
        Returns:
            dict: 投稿結果
        """
        try:
            if access_token:
                # OAuth 2.0トークンを使用
                client = self.create_oauth_client(access_token)
            else:
                # 従来のアクセストークンを使用
                client = self.client
                
            response = client.create_tweet(text=text)
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