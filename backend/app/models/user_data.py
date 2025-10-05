from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime, timezone
import enum

from app.core.database import Base

class RuleType(enum.Enum):
    SERIES = "series"
    KEYWORD = "keyword"
    TEAM = "team"

class Favourite(Base):
    __tablename__ = "favourites"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    program_id = Column(String, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Rule(Base):
    __tablename__ = "rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    type = Column(Enum(RuleType), nullable=False)
    query = Column(Text)  # For keyword/team rules
    program_id = Column(String)  # For series rules
    station_ids = Column(ARRAY(String))  # Limit to specific stations
    new_only = Column(Boolean, default=True)
    padding_pre = Column(Integer, default=0)  # Minutes before
    padding_post = Column(Integer, default=0)  # Minutes after
    keep_last = Column(Integer)  # Number of recordings to keep
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    rule_id = Column(UUID(as_uuid=True), index=True)
    station_id = Column(String)
    program_id = Column(String)
    start_utc = Column(DateTime(timezone=True))
    status = Column(String, default="pending")  # pending, sent, suppressed
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))