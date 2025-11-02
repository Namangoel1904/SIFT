"""Service for crawling web pages with enhanced text extraction."""
import httpx
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import io
from ..config import settings
from ..services.utils import (
    is_valid_url, normalize_url, extract_domain
)

logger = logging.getLogger(__name__)


class Crawler:
    """Web crawler for fetching and parsing web pages."""
    
    def __init__(self):
        """Initialize crawler."""
        self.timeout = settings.REQUEST_TIMEOUT
        self.max_retries = settings.MAX_RETRIES
        self.max_depth = settings.MAX_CRAWL_DEPTH
    
    def _extract_text_from_semantic_tags(self, soup: BeautifulSoup) -> str:
        """Extract text from semantic HTML tags: <article>, <main>, or largest <p> cluster."""
        text_content = ""
        
        # Priority 1: Try <article> tag
        article = soup.find('article')
        if article:
            # Remove script and style elements
            for script in article.find_all(["script", "style", "nav", "aside", "header", "footer"]):
                script.decompose()
            text_content = article.get_text(separator=' ', strip=True)
            if len(text_content) > 100:  # Ensure we got substantial content
                return text_content
        
        # Priority 2: Try <main> tag
        main = soup.find('main')
        if main:
            for script in main.find_all(["script", "style", "nav", "aside", "header", "footer"]):
                script.decompose()
            text_content = main.get_text(separator=' ', strip=True)
            if len(text_content) > 100:
                return text_content
        
        # Priority 3: Find largest <p> cluster
        paragraphs = soup.find_all('p')
        if paragraphs:
            # Group consecutive paragraphs
            clusters = []
            current_cluster = []
            current_length = 0
            
            for p in paragraphs:
                p_text = p.get_text(strip=True)
                if len(p_text) < 10:  # Skip very short paragraphs
                    continue
                
                # If this paragraph is close to previous, add to cluster
                if current_length > 0 and len(current_cluster) > 0:
                    current_cluster.append(p_text)
                    current_length += len(p_text)
                else:
                    # Start new cluster
                    if current_cluster:
                        clusters.append((current_length, ' '.join(current_cluster)))
                    current_cluster = [p_text]
                    current_length = len(p_text)
            
            # Add last cluster
            if current_cluster:
                clusters.append((current_length, ' '.join(current_cluster)))
            
            # Get largest cluster
            if clusters:
                clusters.sort(key=lambda x: x[0], reverse=True)
                text_content = clusters[0][1]
                if len(text_content) > 100:
                    return text_content
        
        # Fallback: Extract all text from body
        body = soup.find('body')
        if body:
            for script in body.find_all(["script", "style", "nav", "aside", "header", "footer"]):
                script.decompose()
            return body.get_text(separator=' ', strip=True)
        
        return ""
    
    async def _extract_pdf_content(self, url: str, content: bytes) -> Optional[str]:
        """Extract text content from PDF."""
        try:
            # Try PyPDF2 first
            try:
                import PyPDF2
                pdf_file = io.BytesIO(content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
            except ImportError:
                pass
            
            # Try pdfplumber as fallback
            try:
                import pdfplumber
                pdf_file = io.BytesIO(content)
                with pdfplumber.open(pdf_file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text.strip()
            except ImportError:
                pass
            
            # If no PDF library available, return None
            print(f"PDF libraries not available. Install PyPDF2 or pdfplumber for PDF support.")
            return None
            
        except Exception as e:
            print(f"Error extracting PDF content: {e}")
            return None
    
    async def fetch_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch a single URL and return parsed content with enhanced text extraction."""
        if not is_valid_url(url):
            return None
        
        # Modern browser User-Agent header
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                    
                    content_type = response.headers.get("content-type", "").lower()
                    
                    # Handle PDF files
                    if "application/pdf" in content_type or url.lower().endswith('.pdf'):
                        pdf_content = await self._extract_pdf_content(url, response.content)
                        if pdf_content:
                            return {
                                "url": normalize_url(url),
                                "title": url.split('/')[-1] or "PDF Document",
                                "description": pdf_content[:200] + "..." if len(pdf_content) > 200 else pdf_content,
                                "text": pdf_content,
                                "html": "",
                                "status_code": response.status_code,
                                "content_type": "pdf"
                            }
                    
                    # Handle HTML content
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract title and description first (needed for fallback)
                    title = ""
                    if soup.title:
                        title = soup.title.string or ""
                    else:
                        og_title = soup.find("meta", property="og:title")
                        if og_title:
                            title = og_title.get("content", "")
                        else:
                            h1 = soup.find("h1")
                            if h1:
                                title = h1.get_text(strip=True)
                    
                    description = ""
                    meta_desc = soup.find("meta", {"name": "description"})
                    if meta_desc:
                        description = meta_desc.get("content", "")
                    else:
                        og_desc = soup.find("meta", property="og:description")
                        if og_desc:
                            description = og_desc.get("content", "")
                        else:
                            # Use first paragraph as description
                            first_p = soup.find("p")
                            if first_p:
                                description = first_p.get_text(strip=True)[:200]
                    
                    # Extract text using semantic tags
                    text = self._extract_text_from_semantic_tags(soup)
                    
                    # Clean up text
                    import re
                    text = re.sub(r'\s+', ' ', text)
                    text = text.strip()
                    
                    # Fallback: If no readable text but we have title/description, use those
                    if not text or len(text) < 50:
                        # Combine title and description as minimal context
                        fallback_text = f"{title}. {description}".strip()
                        if len(fallback_text) > 10:
                            text = fallback_text
                            logger.warning(f"Limited text extracted from {url}, using title/description fallback")
                    
                    return {
                        "url": normalize_url(url),
                        "title": title.strip(),
                        "description": description.strip(),
                        "text": text,
                        "html": html[:50000],  # Limit HTML size
                        "status_code": response.status_code,
                        "content_type": "html"
                    }
            
            except httpx.TimeoutException:
                if attempt == self.max_retries - 1:
                    logger.warning(f"Timeout fetching {url}")
                continue
            except httpx.HTTPStatusError as e:
                if attempt == self.max_retries - 1:
                    logger.warning(f"HTTP {e.response.status_code} error fetching {url}")
                continue
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.warning(f"Error fetching {url}: {e}")
                continue
        
        return None
    
    async def fetch_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch multiple URLs concurrently."""
        import asyncio
        
        tasks = [self.fetch_url(url) for url in urls[:10]]  # Limit concurrent requests
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None and exceptions
        valid_results = []
        for result in results:
            if result and isinstance(result, dict):
                valid_results.append(result)
        
        return valid_results
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract links from HTML."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                absolute_url = urljoin(base_url, href)
                
                if is_valid_url(absolute_url):
                    normalized = normalize_url(absolute_url)
                    if normalized not in links:
                        links.append(normalized)
            
            return links[:50]  # Limit links
        except Exception:
            return []
