from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Date, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    twofa_secret = Column(String, nullable=True)
    timezone = Column(String, default="UTC")
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class SchedulesDirectAccount(Base):
    __tablename__ = "sd_accounts"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    sd_username = Column(String, nullable=False)
    sd_token = Column(Text, nullable=False)  # Encrypted
    token_expires_at = Column(DateTime(timezone=True))
    last_success = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Lineup(Base):
    __tablename__ = "lineups"
    
    id = Column(String, primary_key=True)  # SD lineup id
    name = Column(String)
    location = Column(String)
    transport = Column(String)  # Cable, Antenna, Satellite
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class UserLineup(Base):
    __tablename__ = "user_lineups"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    lineup_id = Column(String, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Station(Base):
    __tablename__ = "stations"
    
    id = Column(String, primary_key=True)  # SD station id
    callsign = Column(String)
    name = Column(String)
    affiliate = Column(String)
    is_hd = Column(Boolean, default=False)
    logo_uri = Column(String)
    logo_width = Column(Integer)
    logo_height = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class LineupStation(Base):
    __tablename__ = "lineup_stations"
    
    lineup_id = Column(String, primary_key=True)
    station_id = Column(String, primary_key=True)
    channel = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Program(Base):
    __tablename__ = "programs"
    
    program_id = Column(String, primary_key=True)
    title = Column(String, nullable=False, index=True)
    episode_title = Column(String)
    description = Column(Text)
    season = Column(Integer)
    episode = Column(Integer)
    original_air_date = Column(Date)
    genres = Column(ARRAY(String))
    advisories = Column(ARRAY(String))
    cast = Column(JSON)
    crew = Column(JSON)
    md5 = Column(String, index=True)  # For deduplication
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Schedule(Base):
    __tablename__ = "schedules"
    
    station_id = Column(String, primary_key=True)
    program_id = Column(String, primary_key=True)
    start_utc = Column(DateTime(timezone=True), primary_key=True, index=True)
    end_utc = Column(DateTime(timezone=True), nullable=False, index=True)
    is_new = Column(Boolean, default=False)
    live = Column(Boolean, default=False)
    premiere = Column(Boolean, default=False)
    finale = Column(Boolean, default=False)
    audio = Column(String)  # Stereo, DD 5.1, etc.
    aspect = Column(String)  # 16:9, 4:3
    subtitles = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Image(Base):
    __tablename__ = "images"
    
    ref_id = Column(String, primary_key=True)
    program_id = Column(String, index=True)
    category = Column(String)  # poster, banner, icon
    aspect = Column(String)    # 16x9, 2x3
    uri = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))