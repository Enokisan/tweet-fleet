from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.github_service import GitHubService
from app.core.security import verify_token

router = APIRouter()
github_service = GitHubService()

class NoteRequest(BaseModel):
    content: str

@router.post("/save")
async def save_note(
    note: NoteRequest,
    token: dict = Depends(verify_token)
):
    """
    ノートをGitHubに保存する
    JWT認証が必要
    """
    try:
        result = github_service.save_note(
            content=note.content
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 