from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DB_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    poolclass=StaticPool if "sqlite" in settings.DB_URL else None,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DB_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()