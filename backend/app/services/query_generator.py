"""Service for generating search queries from claims."""
from typing import List, Dict, Any
from ..services.llm_analyzer import LLMAnalyzer


class QueryGenerator:
    """Generate search queries for fact-checking."""
    
    def __init__(self, llm_analyzer: LLMAnalyzer):
        """Initialize query generator."""
        self.llm_analyzer = llm_analyzer
    
    async def generate_queries(self, claim: str, claim_type: str = None) -> List[str]:
        """Generate search queries for fact-checking a claim."""
        if not claim or len(claim.strip()) < 5:
            return []
        
        prompt = f"""Generate 3-5 simple, concise search queries to fact-check the following claim.
        
        Claim: "{claim}"
        Claim Type: {claim_type or "general"}
        
        Guidelines:
        - Extract key factual elements only (keywords, names, numbers, places)
        - Keep queries simple and short (3-7 words maximum)
        - DO NOT include phrases like "fact check", "verified", or "snopes"
        - Use keywords, not full sentences
        - Focus on the core factual claim being made
        
        Examples:
        - Claim: "The Earth is flat" → Query: "Earth flat"
        - Claim: "COVID-19 vaccine causes autism" → Query: "COVID vaccine autism"
        - Claim: "NASA faked the moon landing" → Query: "NASA moon landing"
        
        Return a JSON array of query strings.
        Format: {{"queries": ["query1", "query2", ...]}}"""
        
        try:
            response = await self.llm_analyzer.analyze(prompt, response_format="json")
            if isinstance(response, dict) and "queries" in response:
                queries = response["queries"]
                # Ensure we return a list of strings
                if isinstance(queries, list):
                    return [str(q) for q in queries if q][:5]
            elif isinstance(response, list):
                return [str(q) for q in response if q][:5]
        except Exception as e:
            print(f"Error generating queries: {e}")
        
        # Fallback: simple query generation
        return self._generate_queries_fallback(claim)
    
    def _generate_queries_fallback(self, claim: str) -> List[str]:
        """Fallback query generation - simple keyword extraction."""
        import re
        
        # Remove common stop words and extract keywords
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
                     "of", "with", "is", "was", "are", "were", "been", "be", "have", "has", "had",
                     "do", "does", "did", "will", "would", "could", "should", "may", "might"}
        
        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b\w+\b', claim.lower())
        
        # Filter out stop words and keep meaningful keywords
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:8]
        
        # Create simple queries with 3-7 keywords
        queries = []
        if len(keywords) >= 3:
            # Different combinations of keywords
            queries.append(" ".join(keywords[:4]))  # First 4 keywords
            queries.append(" ".join(keywords[:6]))  # First 6 keywords
            queries.append(" ".join(keywords[:7]))  # First 7 keywords
            if len(keywords) > 4:
                queries.append(" ".join(keywords[2:6]))  # Middle keywords
        else:
            # If too few keywords, use what we have
            queries.append(" ".join(keywords))
        
        # Always include the simplest version
        if keywords:
            queries.append(" ".join(keywords[:3]))
        
        return queries[:5] if queries else [claim[:50]]  # Fallback to first 50 chars

