from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from ....services.twitter import twitter_service
from ....services.twitter_oauth import TwitterOAuthService
from ....core.config import get_settings
from ....core.security import create_access_token
from ....database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import json
import urllib.parse

router = APIRouter()
settings = get_settings()
twitter_oauth_service = TwitterOAuthService()

# セッション情報を一時的に保存するための簡易ストレージ
# 本番環境ではRedisなどを使用することを推奨
session_storage = {}

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

@router.get("/auth/twitter/oauth")
async def twitter_oauth_start():
    """
    Twitter OAuth 2.0認証を開始
    """
    try:
        # 設定確認
        print(f"Twitter Client ID: {settings.TWITTER_CLIENT_ID[:10] if settings.TWITTER_CLIENT_ID else 'None'}...")
        print(f"Twitter Redirect URI: {settings.TWITTER_REDIRECT_URI}")
        
        auth_data = twitter_oauth_service.generate_authorization_url()
        
        # セッション情報を保存（本番環境ではRedisなどを使用）
        session_storage[auth_data["state"]] = {
            "code_verifier": auth_data["code_verifier"]
        }
        
        print(f"Generated authorization URL: {auth_data['authorization_url']}")
        
        return {
            "authorization_url": auth_data["authorization_url"],
            "state": auth_data["state"]
        }
    except Exception as e:
        print(f"Twitter OAuth start error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Twitter OAuth認証の開始に失敗しました: {str(e)}"
        )

@router.get("/auth/twitter/callback")
async def twitter_oauth_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Twitter OAuth 2.0認証のコールバック処理
    """
    try:
        # セッション情報を取得
        session_data = session_storage.get(state)
        if not session_data:
            # エラーをフロントエンドに渡してリダイレクト
            frontend_url = settings.FRONTEND_URL or "http://localhost:5174"
            error_message = urllib.parse.quote("無効な状態パラメータです")
            return RedirectResponse(
                url=f"{frontend_url}/auth/callback?error={error_message}",
                status_code=302
            )
        
        # 認証コードをアクセストークンに交換
        result = await twitter_oauth_service.exchange_code_for_tokens(
            code=code,
            code_verifier=session_data["code_verifier"],
            db=db
        )
        
        # セッション情報をクリア
        del session_storage[state]
        
        # JWTトークンを発行
        access_token = create_access_token(
            data={"sub": str(result["user"].id), "username": result["user"].username}
        )
        
        # 認証成功時はフロントエンドにリダイレクト（トークンをクエリパラメータで渡す）
        frontend_url = settings.FRONTEND_URL or "http://localhost:5174"
        token_encoded = urllib.parse.quote(access_token)
        username_encoded = urllib.parse.quote(result["user"].username)
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?token={token_encoded}&username={username_encoded}",
            status_code=302
        )
        
    except Exception as e:
        # エラー時はセッション情報をクリア
        if state in session_storage:
            del session_storage[state]
        
        # エラーをフロントエンドに渡してリダイレクト
        frontend_url = settings.FRONTEND_URL or "http://localhost:5174"
        error_message = urllib.parse.quote(f"Twitter OAuth認証に失敗しました: {str(e)}")
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?error={error_message}",
            status_code=302
        ) 