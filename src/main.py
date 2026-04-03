"""
FastAPI application instance and configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.database import engine, Base
from src.config import settings
from src.utils.logging_config import setup_logging
from src.api import employees

# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="社員情報 CRUD API",
    description="FastAPI ベースの社員情報管理 REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    """Create database tables on startup"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")


# Include routers
app.include_router(employees.router, prefix="/api/v1", tags=["employees"])


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
