"""Routes for text analysis and fact-checking."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from ..services.factcheck_service import FactCheckService

router = APIRouter()


class AnalyzeRequest(BaseModel):
    """Request model for text analysis."""
    text: str = Field(..., description="Text to analyze and fact-check", min_length=10)
    url: Optional[str] = Field(None, description="Optional URL source of the text")


class AnalyzeURLRequest(BaseModel):
    """Request model for URL analysis."""
    url: str = Field(..., description="URL to analyze and fact-check")


# Initialize service
factcheck_service = FactCheckService()


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    """Analyze text and fact-check claims.
    
    Returns structured JSON with claims, verdicts, confidence scores, explanations, and citations.
    """
    try:
        result = await factcheck_service.analyze_text(request.text, request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/url")
async def analyze_url(request: AnalyzeURLRequest):
    """Analyze URL and fact-check claims from the page content.
    
    Fetches content from the URL (supports HTML and PDF), extracts text,
    and runs the same fact-checking pipeline as text analysis.
    
    Returns structured JSON with claims, verdicts, confidence scores, explanations, and citations.
    """
    try:
        result = await factcheck_service.factcheck_url(request.url)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SIFT API"
    }

