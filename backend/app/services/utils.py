"""Utility functions for the SIFT backend."""
import re
import hashlib
from typing import List, Dict, Any
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:-]', '', text)
    return text.strip()


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def normalize_url(url: str) -> str:
    """Normalize URL for comparison."""
    parsed = urlparse(url)
    # Remove fragment and normalize
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        normalized += f"?{parsed.query}"
    return normalized.rstrip('/')


def extract_text_from_html(html: str) -> str:
    """Extract clean text from HTML."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        # Get text
        text = soup.get_text()
        return clean_text(text)
    except Exception:
        return ""


def chunk_text(text: str, max_length: int = 1000) -> List[str]:
    """Split text into chunks of maximum length."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    sentences = re.split(r'[.!?]\s+', text)
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def generate_hash(text: str) -> str:
    """Generate hash for text."""
    return hashlib.md5(text.encode()).hexdigest()


def deduplicate_list(items: List[Any]) -> List[Any]:
    """Remove duplicates from list while preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def merge_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge multiple fact-check results."""
    if not results:
        return {}
    
    merged = {
        "claims": [],
        "verdicts": [],
        "sources": [],
        "confidence": 0.0
    }
    
    for result in results:
        if isinstance(result, dict):
            merged["claims"].extend(result.get("claims", []))
            merged["verdicts"].extend(result.get("verdicts", []))
            merged["sources"].extend(result.get("sources", []))
    
    # Deduplicate
    merged["claims"] = deduplicate_list(merged["claims"])
    merged["verdicts"] = deduplicate_list(merged["verdicts"])
    merged["sources"] = deduplicate_list(merged["sources"])
    
    # Calculate average confidence
    if results:
        confidences = [r.get("confidence", 0.0) for r in results if isinstance(r, dict)]
        merged["confidence"] = sum(confidences) / len(confidences) if confidences else 0.0
    
    return merged

