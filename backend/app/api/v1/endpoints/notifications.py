from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.sd import get_current_user
from app.models.core import User

router = APIRouter()

@router.get("/")
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    return {"message": "Get notifications endpoint - implementation needed"}
