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
    # For local development: path to credentials file
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # For Render deployment: JSON string from environment variable
    GOOGLE_CREDENTIALS_JSON: Optional[str] = os.getenv("GOOGLE_CREDENTIALS_JSON")
    
    # Cache Settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Crawler Settings
    MAX_CRAWL_DEPTH: int = 2
    REQUEST_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    
    # Fact-checking Settings
    FACTCHECK_PROVIDERS: list = ["factcheck.org", "snopes", "politifact"]
    
    # CORS Settings
    # Note: FastAPI CORS doesn't support wildcards, so use specific origins or ["*"] for all
    # Default CORS origins for local development
    _DEFAULT_CORS_ORIGINS = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # CORS_ORIGINS from environment variable (comma-separated string)
    # Don't define as list type to avoid Pydantic JSON parsing issues
    CORS_ORIGINS: Optional[str] = None
    
    @property
    def cors_origins(self) -> list:
        """Get CORS origins including environment-based additions.
        
        For production, set CORS_ORIGINS environment variable with comma-separated URLs.
        Example: CORS_ORIGINS=https://your-app.netlify.app,https://another-domain.com
        """
        import logging
        logger = logging.getLogger(__name__)
        
        origins = self._DEFAULT_CORS_ORIGINS.copy()
        
        # Parse environment variable (comma-separated string)
        env_origins = os.getenv("CORS_ORIGINS") or self.CORS_ORIGINS
        logger.info(f"Raw CORS_ORIGINS env var: {repr(env_origins)}")
        
        if env_origins:
            parsed_origins = [origin.strip() for origin in env_origins.split(",") if origin.strip()]
            origins.extend(parsed_origins)
            logger.info(f"Parsed additional CORS origins: {parsed_origins}")
        
        # Allow all origins if explicitly set (for quick testing)
        if os.getenv("ALLOW_ALL_ORIGINS", "").lower() == "true":
            logger.warning("ALLOW_ALL_ORIGINS is set to true - allowing all origins")
            return ["*"]
        
        logger.info(f"Final CORS origins list: {origins}")
        return origins
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

