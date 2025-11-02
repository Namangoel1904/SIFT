"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import analyze



app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="SIFT API - AI misinformation prevention & fact-checking"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

