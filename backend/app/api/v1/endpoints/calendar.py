from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.sd import get_current_user
from app.models.core import User

router = APIRouter()

@router.get("/ical")
async def get_ical_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get iCal feed for user's calendar"""
    return Response(
        content="BEGIN:VCALENDAR\nVERSION:2.0\nEND:VCALENDAR",
        media_type="text/calendar"
    )
