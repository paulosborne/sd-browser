from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.sd import get_current_user
from app.models.core import User

router = APIRouter()

@router.get("/jobs")
async def get_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get background job status"""
    return {"message": "Admin jobs endpoint - implementation needed"}

@router.get("/health")
async def admin_health():
    """Admin health check"""
    return {"status": "healthy"}
