from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    APP_ENV: str = "development"
    APP_BASE_URL: str = "http://localhost:3000"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Database
    DB_URL: str = "postgresql://sd_user:sd_password@localhost:5432/sd_browser"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    JWT_SECRET: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_EXPIRE_DAYS: int = 30
    ENCRYPTION_KEY: str = "dev-encryption-key-32-chars-long"
    
    # Schedules Direct
    SD_API_BASE: str = "https://json.schedulesdirect.org/20141201"
    SD_APPID: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Email (optional)
    EMAIL_SMTP_URI: Optional[str] = None
    
    # Object Storage (optional)
    OBJECT_STORAGE_URI: str = "file:///tmp/exports"
    
    # RQ Dashboard
    RQ_DASHBOARD_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()