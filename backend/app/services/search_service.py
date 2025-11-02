"""Service for searching the web using Fact Check Tools API and Google Custom Search."""
import httpx
import logging
from typing import List, Dict, Any
from ..config import settings
from ..services.utils import is_valid_url, normalize_url

logger = logging.getLogger(__name__)


class SearchService:
    """Service for web search using multiple APIs."""
    
    def __init__(self):
        """Initialize search service."""
        self.fact_check_api_key = settings.FACT_CHECK_API_KEY
        self.google_search_api_key = settings.GOOGLE_SEARCH_API_KEY
        self.google_search_cx = settings.GOOGLE_SEARCH_CX
    
    def _simplify_claim(self, text: str) -> str:
        """Remove stopwords to create a simpler query."""
        STOPWORDS = {
            "is", "are", "was", "were", "the", "that", "because", "do", "does", "did",
            "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "have", "has", "had", "will", "would", "could", "should", "may", "might",
            "this", "these", "those", "they", "them", "their", "there"
        }
        words = text.split()
        simplified = " ".join(w for w in words if w.lower() not in STOPWORDS)
        return simplified if simplified else text  # Fallback to original if empty
    
    async def search_factcheck_api(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Google Fact Check Tools API with fallback retries.
        
        Returns empty list if no results found, but logs as debug.
        This allows the system to continue with other evidence sources.
        """
        if not self.fact_check_api_key:
            return []
        
        FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        
        # Prepare base parameters
        base_params = {
            "key": self.fact_check_api_key,
            "query": query,
            "languageCode": "en-US",
            "pageSize": 5,  # Use fixed pageSize=5 as specified
            "maxAgeDays": 365,
        }
        
        # Define retry attempts with different strategies
        attempts = [
            {
                "params": base_params,
                "description": "original query with date filter"
            },
            {
                "params": {**base_params, "maxAgeDays": None},  # Remove date filter
                "description": "without date limit"
            },
            {
                "params": {
                    "key": self.fact_check_api_key,
                    "query": self._simplify_claim(query),
                    "languageCode": "en-US",
                    "pageSize": 3,  # Lower page size for simplified query
                },
                "description": "simplified query (no stopwords)"
            },
        ]
        
        # Filter out None values from params and try each attempt
        async with httpx.AsyncClient(timeout=10.0) as client:
            for attempt_idx, attempt in enumerate(attempts):
                # Filter out None values from params
                params = {k: v for k, v in attempt["params"].items() if v is not None}
                description = attempt["description"]
                
                logger.debug(f"FactCheck API attempt {attempt_idx + 1}: {description} | Query: {params.get('query', '')[:50]}")
                
                try:
                    response = await client.get(FACTCHECK_URL, params=params)
                    
                    # Handle 403 gracefully - treat as "no facts found", not a failure
                    if response.status_code == 403:
                        logger.debug(f"Fact Check API returned 403 (no facts found) for attempt {attempt_idx + 1}: {description}")
                        continue  # Try next attempt
                    
                    # Check if successful
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            claims = data.get("claims", [])
                            
                            if claims:
                                logger.debug(f"FactCheck API success on attempt {attempt_idx + 1} ({description}): found {len(claims)} claims")
                                # Parse and return results (same format as before)
                                results = []
                                for claim in claims[:max_results]:
                                    # Extract claim review information
                                    review_urls = []
                                    review_texts = []
                                    
                                    for review in claim.get("claimReview", []):
                                        publisher = review.get("publisher", {})
                                        review_urls.append(review.get("url", ""))
                                        
                                        # Extract review text
                                        text = review.get("textualRating", "") or publisher.get("name", "")
                                        if text:
                                            review_texts.append(text)
                                    
                                    # Get the first URL or use claim URL
                                    url = claim.get("claimant", "") or ""
                                    if review_urls:
                                        url = review_urls[0]
                                    
                                    results.append({
                                        "title": claim.get("text", "")[:100] or "Fact Check",
                                        "url": url,
                                        "snippet": " ".join(review_texts[:2])[:300] if review_texts else claim.get("text", "")[:300],
                                        "source": "fact_check_api",
                                        "claim_original": claim.get("text", ""),
                                        "fact_check_reviews": review_urls
                                    })
                                
                                return results
                            else:
                                logger.debug(f"FactCheck API attempt {attempt_idx + 1} ({description}): 0 claims in response")
                                continue  # Try next attempt
                                
                        except Exception as parse_error:
                            logger.warning(f"FactCheck API parse error on attempt {attempt_idx + 1}: {parse_error} | Status: {response.status_code}")
                            continue
                    else:
                        # Non-200, non-403, non-503 status code
                        error_text = ""
                        try:
                            error_data = response.json()
                            error_text = f" | API message: {error_data}"
                        except:
                            error_text = f" | Response text: {response.text[:200]}"
                        
                        if response.status_code == 503:
                            logger.warning(f"FactCheck API returned 503 (service unavailable) on attempt {attempt_idx + 1} ({description}){error_text} - continuing with other sources")
                        else:
                            logger.warning(f"FactCheck API HTTP {response.status_code} on attempt {attempt_idx + 1} ({description}){error_text}")
                        continue  # Try next attempt
                        
                except httpx.TimeoutException as e:
                    logger.warning(f"FactCheck API timeout on attempt {attempt_idx + 1} ({description}): {e}")
                    continue
                except httpx.HTTPStatusError as e:
                    status_code = e.response.status_code
                    error_text = ""
                    try:
                        error_data = e.response.json()
                        error_text = f" | API message: {error_data}"
                    except:
                        error_text = f" | Response text: {e.response.text[:200]}"
                    
                    if status_code == 403:
                        logger.debug(f"FactCheck API 403 on attempt {attempt_idx + 1} ({description}): no facts found{error_text}")
                    elif status_code == 503:
                        logger.warning(f"FactCheck API 503 (service unavailable) on attempt {attempt_idx + 1} ({description}){error_text} - continuing with other sources")
                    else:
                        logger.warning(f"FactCheck API HTTP {status_code} on attempt {attempt_idx + 1} ({description}){error_text}")
                    continue
                except Exception as e:
                    logger.warning(f"FactCheck API error on attempt {attempt_idx + 1} ({description}): {type(e).__name__}: {e}")
                    continue
        
        # All attempts exhausted
        logger.debug(f"FactCheck API: No results found after {len(attempts)} attempts for query: {query[:50]}")
        return []
    
    async def search_google_custom(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Google Custom Search API."""
        if not self.google_search_api_key or not self.google_search_cx:
            return []
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": self.google_search_api_key,
                    "cx": self.google_search_cx,
                    "q": query,
                    "num": min(num_results, 10)  # Google API limit
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                results = []
                for item in data.get("items", [])[:num_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "source": "google_custom_search"
                    })
                
                return results
        except Exception as e:
            print(f"Google Custom Search error: {e}")
            return []
    
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using all available APIs."""
        all_results = []
        
        # Try Fact Check API first
        fact_check_results = await self.search_factcheck_api(query, num_results // 2)
        all_results.extend(fact_check_results)
        
        # Then try Google Custom Search
        google_results = await self.search_google_custom(query, num_results - len(all_results))
        all_results.extend(google_results)
        
        return all_results[:num_results]
    
    def is_factcheck_source(self, url: str) -> bool:
        """Check if URL is from a known fact-checking source."""
        factcheck_domains = [
            "factcheck.org",
            "snopes.com",
            "politifact.com",
            "factchecker.in",
            "fullfact.org",
            "africacheck.org",
            "checkyourfact.com",
            "leadstories.com"
        ]
        
        url_lower = url.lower()
        return any(domain in url_lower for domain in factcheck_domains)
    
    async def search_factcheck_sources(self, query: str) -> List[Dict[str, Any]]:
        """Search specifically in fact-checking sources."""
        # First try Fact Check API
        results = await self.search_factcheck_api(query, 5)
        
        # Then try Google Custom Search with fact-check site filters
        factcheck_query = f"{query} site:factcheck.org OR site:snopes.com OR site:politifact.com"
        google_results = await self.search_google_custom(factcheck_query, 5)
        results.extend(google_results)
        
        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for result in results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
