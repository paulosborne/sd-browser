from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.core.security import verify_token, encrypt_data, decrypt_data
from app.models.core import User, SchedulesDirectAccount, Lineup, UserLineup
from app.services.schedules_direct import SchedulesDirectClient
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

class SDConnectRequest(BaseModel):
    sd_username: str
    sd_password: str

class LineupResponse(BaseModel):
    id: str
    name: str
    location: str
    transport: Optional[str] = None

class SDConnectionResponse(BaseModel):
    connected: bool
    username: Optional[str] = None
    last_success: Optional[str] = None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    try:
        payload = verify_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/connect", response_model=SDConnectionResponse)
async def connect_sd_account(
    request: SDConnectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect user's Schedules Direct account"""
    try:
        # Initialize SD client and authenticate
        sd_client = SchedulesDirectClient(settings.SD_API_BASE)
        token_data = await sd_client.authenticate(request.sd_username, request.sd_password)
        
        # Encrypt and store the token
        encrypted_token = encrypt_data(token_data["token"])
        
        # Check if account already exists
        sd_account = db.query(SchedulesDirectAccount).filter(
            SchedulesDirectAccount.user_id == current_user.id
        ).first()
        
        if sd_account:
            # Update existing account
            sd_account.sd_username = request.sd_username
            sd_account.sd_token = encrypted_token
            sd_account.token_expires_at = token_data.get("expires_at")
        else:
            # Create new account
            sd_account = SchedulesDirectAccount(
                user_id=current_user.id,
                sd_username=request.sd_username,
                sd_token=encrypted_token,
                token_expires_at=token_data.get("expires_at")
            )
            db.add(sd_account)
        
        db.commit()
        
        return SDConnectionResponse(
            connected=True,
            username=request.sd_username
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to connect SD account: {str(e)}"
        )

@router.get("/status", response_model=SDConnectionResponse)
async def get_sd_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get Schedules Direct connection status"""
    sd_account = db.query(SchedulesDirectAccount).filter(
        SchedulesDirectAccount.user_id == current_user.id
    ).first()
    
    if not sd_account:
        return SDConnectionResponse(connected=False)
    
    return SDConnectionResponse(
        connected=True,
        username=sd_account.sd_username,
        last_success=sd_account.last_success.isoformat() if sd_account.last_success else None
    )

@router.get("/lineups", response_model=List[LineupResponse])
async def get_available_lineups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get available lineups for the user's SD account"""
    sd_account = db.query(SchedulesDirectAccount).filter(
        SchedulesDirectAccount.user_id == current_user.id
    ).first()
    
    if not sd_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Schedules Direct account connected"
        )
    
    try:
        # Decrypt token and get lineups
        token = decrypt_data(sd_account.sd_token)
        sd_client = SchedulesDirectClient(settings.SD_API_BASE)
        lineups = await sd_client.get_lineups(token)
        
        # Update last success
        from datetime import datetime, timezone
        sd_account.last_success = datetime.now(timezone.utc)
        db.commit()
        
        return [
            LineupResponse(
                id=lineup["lineup"],
                name=lineup.get("name", ""),
                location=lineup.get("location", ""),
                transport=lineup.get("transport")
            )
            for lineup in lineups
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch lineups: {str(e)}"
        )

@router.post("/lineups")
async def add_lineup(
    lineup_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a lineup to user's selection"""
    # Check if lineup exists
    lineup = db.query(Lineup).filter(Lineup.id == lineup_id).first()
    if not lineup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lineup not found"
        )
    
    # Check if already added
    existing = db.query(UserLineup).filter(
        UserLineup.user_id == current_user.id,
        UserLineup.lineup_id == lineup_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lineup already added"
        )
    
    # Add lineup
    user_lineup = UserLineup(user_id=current_user.id, lineup_id=lineup_id)
    db.add(user_lineup)
    db.commit()
    
    return {"message": "Lineup added successfully"}

@router.delete("/lineups/{lineup_id}")
async def remove_lineup(
    lineup_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a lineup from user's selection"""
    user_lineup = db.query(UserLineup).filter(
        UserLineup.user_id == current_user.id,
        UserLineup.lineup_id == lineup_id
    ).first()
    
    if not user_lineup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lineup not found in user's selection"
        )
    
    db.delete(user_lineup)
    db.commit()
    
    return {"message": "Lineup removed successfully"}