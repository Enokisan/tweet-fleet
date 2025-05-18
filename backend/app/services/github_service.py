from github import Github
from datetime import datetime
import os
from typing import Optional
import logging
from ..core.config import get_settings

# ロガーの設定
logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        settings = get_settings()
        self.github_token = settings.GITHUB_TOKEN
        logger.info(f"GITHUB_TOKEN exists: {self.github_token is not None}")
        
        self.github = Github(self.github_token) if self.github_token else None
        self.repo_name = settings.GITHUB_REPO
        self.directory_path = settings.GITHUB_DIRECTORY_PATH
        
        # GitHub接続テスト
        if self.github:
            try:
                self.github.get_user()
                logger.info("GitHub authentication successful")
            except Exception as e:
                logger.error(f"GitHub authentication failed: {str(e)}")
                self.github = None

    def save_note(self, content: str) -> dict:
        """
        ノートをGitHubリポジトリに保存する
        
        Args:
            content (str): 保存するノートの内容
            
        Returns:
            dict: 保存結果の情報
        """
        logger.info("Attempting to save note to GitHub")
        
        if not self.github:
            logger.error("GitHub authentication not configured")
            raise Exception("GitHub認証が設定されていません")
        
        if not self.repo_name:
            logger.error("GitHub repository not configured")
            raise Exception("GitHubリポジトリが設定されていません")

        try:
            # リポジトリの取得
            logger.info(f"Attempting to get repository: {self.repo_name}")
            repo = self.github.get_repo(self.repo_name)
            
            # 現在時刻を取得してファイル名を生成
            now = datetime.now()
            filename = now.strftime("%Y%m%d%H%M%S.md")
            
            # 完全なファイルパスを生成
            full_path = os.path.join(self.directory_path, filename).replace("\\", "/")
            logger.info(f"Creating file at path: {full_path}")
            
            # ファイルの内容を準備
            file_content = f"""---
date: {now.isoformat()}
---

{content}
"""
            
            # ファイルの作成
            repo.create_file(
                path=full_path,
                message=f"Create new note: {now.isoformat()}",
                content=file_content
            )
            
            logger.info(f"Successfully created file at {full_path}")
            return {
                "success": True,
                "message": "ノートを保存しました",
                "repo": self.repo_name,
                "path": full_path
            }
            
        except Exception as e:
            logger.error(f"Failed to save note: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"保存に失敗しました: {str(e)}"
            } 