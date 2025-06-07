from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)  # "twitter", "github"
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_secret = Column(Text, nullable=True)  # Twitter OAuth 1.0a用
    expires_at = Column(DateTime(timezone=True), nullable=True)
    scope = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーションシップ
    user = relationship("User", back_populates="oauth_tokens")

    def is_expired(self) -> bool:
        """トークンが期限切れかどうかを判定"""
        if not self.expires_at:
            return False
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) > self.expires_at 