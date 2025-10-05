from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.sd import get_current_user
from app.models.core import User

router = APIRouter()

@router.post("/{program_id}")
async def add_favourite(
    program_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add program to favourites"""
    return {"message": "Add favourite endpoint - implementation needed"}

@router.delete("/{program_id}")
async def remove_favourite(
    program_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove program from favourites"""
    return {"message": "Remove favourite endpoint - implementation needed"}
