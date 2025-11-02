"""Configuration settings for the SIFT backend."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_TITLE: str = "SIFT API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Google Gemini Settings
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    SIFT_GEMINI_MODEL: str = os.getenv("SIFT_GEMINI_MODEL", "gemini-2.0-flash")
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.1"))
    GEMINI_ENDPOINT: str = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Google Search Settings
    GOOGLE_SEARCH_API_KEY: Optional[str] = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_CX: Optional[str] = os.getenv("GOOGLE_SEARCH_CX")
    
    # Fact Check Tools API
    FACT_CHECK_API_KEY: Optional[str] = os.getenv("FACT_CHECK_API_KEY")

    # Google Cloud Credentials
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Cache Settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Crawler Settings
    MAX_CRAWL_DEPTH: int = 2
    REQUEST_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    
    # Fact-checking Settings
    FACTCHECK_PROVIDERS: list = ["factcheck.org", "snopes", "politifact"]
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "chrome-extension://*",
        "http://localhost:*",
        "http://127.0.0.1:*"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

