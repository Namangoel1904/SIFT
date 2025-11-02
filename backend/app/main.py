"""Main FastAPI application."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import analyze

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="SIFT API - AI misinformation prevention & fact-checking"
)

# Get CORS origins and log them for debugging
cors_origins_list = settings.cors_origins
logger.info(f"CORS origins configured: {cors_origins_list}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, prefix=settings.API_PREFIX, tags=["analysis"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SIFT API - AI Misinformation Prevention & Fact-Checking",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }


@app.get("/cors-debug")
async def cors_debug():
    """Debug endpoint to check CORS configuration."""
    import os
    return {
        "cors_origins": settings.cors_origins,
        "env_cors_origins": os.getenv("CORS_ORIGINS"),
        "allow_all_origins": os.getenv("ALLOW_ALL_ORIGINS"),
        "cors_origins_count": len(settings.cors_origins),
        "message": "CORS Debug Info"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    import os
    return {
        "status": "healthy",
        "cors_configured": len(settings.cors_origins) > 0,
        "cors_origins_count": len(settings.cors_origins),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

