from authlib.integrations.requests_client import OAuth2Session
from typing import Optional, Dict, Any
import secrets
import urllib.parse
from ..core.config import get_settings
from ..models.user import User
from ..models.oauth_token import OAuthToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
import httpx

settings = get_settings()

class TwitterOAuthService:
    def __init__(self):
        self.client_id = settings.TWITTER_CLIENT_ID
        self.client_secret = settings.TWITTER_CLIENT_SECRET
        self.redirect_uri = settings.TWITTER_REDIRECT_URI
        self.authorization_endpoint = "https://twitter.com/i/oauth2/authorize"
        self.token_endpoint = "https://api.twitter.com/2/oauth2/token"
        
    def generate_authorization_url(self) -> Dict[str, str]:
        """OAuth認証URLを生成"""
        if not self.client_id:
            raise ValueError("Twitter Client ID が設定されていません")
            
        # PKCE用のコードベリファイアとチャレンジを生成
        code_verifier = secrets.token_urlsafe(128)
        code_challenge = code_verifier  # プレーンテキスト（ハッシュ化も可能）
        
        # 状態パラメータ
        state = secrets.token_urlsafe(32)
        
        # 認証URLのパラメータ
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "tweet.read tweet.write users.read",  # offline.accessを一時的に削除
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "plain"
        }
        
        auth_url = f"{self.authorization_endpoint}?{urllib.parse.urlencode(params)}"
        
        print(f"OAuth Config Check:")
        print(f"  Client ID: {self.client_id}")
        print(f"  Redirect URI: {self.redirect_uri}")
        print(f"  Authorization URL: {auth_url}")
        
        return {
            "authorization_url": auth_url,
            "state": state,
            "code_verifier": code_verifier
        }
    
    async def exchange_code_for_tokens(
        self, 
        code: str, 
        code_verifier: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """認証コードをアクセストークンに交換"""
        if not self.client_id or not self.client_secret:
            raise ValueError("Twitter OAuth設定が不完全です")
            
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_endpoint,
                data=token_data,
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"トークン取得に失敗: {response.text}")
                
            token_response = response.json()
            
        # ユーザー情報を取得
        user_info = await self._get_user_info(token_response["access_token"])
        
        # ユーザーをデータベースで検索または作成
        user = await self._get_or_create_user(db, user_info)
        
        # トークンを保存
        await self._save_oauth_token(db, user.id, token_response)
        
        return {
            "success": True,
            "user": user,
            "token_info": token_response
        }
    
    async def _get_user_info(self, access_token: str) -> Dict[str, Any]:
        """アクセストークンを使用してユーザー情報を取得"""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.twitter.com/2/users/me",
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"ユーザー情報取得に失敗: {response.text}")
                
            return response.json()["data"]
    
    async def _get_or_create_user(self, db: AsyncSession, user_info: Dict[str, Any]) -> User:
        """ユーザを検索または作成"""
        username = user_info["username"]
        
        # 既存ユーザーを検索
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # 新規ユーザーを作成
            user = User(username=username)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
        return user
    
    async def _save_oauth_token(
        self, 
        db: AsyncSession, 
        user_id: int, 
        token_response: Dict[str, Any]
    ):
        """OAuthトークンを保存"""
        # 既存のTwitterトークンを削除
        existing_tokens = await db.execute(
            select(OAuthToken).where(
                OAuthToken.user_id == user_id,
                OAuthToken.provider == "twitter"
            )
        )
        for token in existing_tokens.scalars():
            await db.delete(token)
        
        # 有効期限を計算
        expires_at = None
        if "expires_in" in token_response:
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_response["expires_in"])
        
        # 新しいトークンを保存
        oauth_token = OAuthToken(
            user_id=user_id,
            provider="twitter",
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
            expires_at=expires_at,
            scope=token_response.get("scope")
        )
        db.add(oauth_token)
        await db.commit()
    
    async def get_user_twitter_token(self, db: AsyncSession, user_id: int) -> Optional[OAuthToken]:
        """ユーザーのTwitterトークンを取得"""
        result = await db.execute(
            select(OAuthToken).where(
                OAuthToken.user_id == user_id,
                OAuthToken.provider == "twitter"
            )
        )
        return result.scalar_one_or_none() 