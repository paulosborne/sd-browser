from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.core.redis import redis_client
from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.core.metrics import setup_metrics

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting SD Browser API")
    
    # Test connections
    try:
        # Test Redis connection
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
    
    # Setup metrics
    setup_metrics(app)
    
    yield
    
    # Shutdown
    logger.info("Shutting down SD Browser API")
    await redis_client.close()

# Create FastAPI app
app = FastAPI(
    title="Schedules Direct EPG Browser",
    description="Production-ready EPG application with Schedules Direct integration",
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV == "development" else None,
    redoc_url="/redoc" if settings.APP_ENV == "development" else None,
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.APP_ENV == "development" else [settings.APP_BASE_URL]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_ENV == "development" else [settings.APP_BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} - {process_time:.3f}s",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "client_ip": request.client.host if request.client else None
        }
    )
    
    return response

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Redis
        await redis_client.ping()
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "redis": redis_status
        }
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Schedules Direct EPG Browser API",
        "version": "1.0.0",
        "docs": "/docs" if settings.APP_ENV == "development" else None
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )