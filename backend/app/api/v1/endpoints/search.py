from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.v1.endpoints.sd import get_current_user
from app.models.core import User

router = APIRouter()

@router.get("/")
async def search_programs(
    q: str = Query(..., description="Search query"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    new_only: Optional[bool] = Query(None, description="Show only new episodes"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search programs and schedules"""
    return {"message": "Search endpoint - implementation needed"}
