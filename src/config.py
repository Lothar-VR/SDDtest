"""
Configuration management for the Employee CRUD API
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    """Application settings from environment variables"""
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./employees.db")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
