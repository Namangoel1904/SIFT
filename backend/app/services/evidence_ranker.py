"""Service for ranking and summarizing evidence snippets with priority levels."""
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from ..services.llm_analyzer import LLMAnalyzer


class EvidenceRanker:
    """Rank and summarize evidence snippets for fact-checking."""
    
    # Priority levels
    PRIORITY_FACT_CHECK_API = 3.0  # Highest priority
    PRIORITY_GOV_EDU_NEWS = 2.0    # Medium-high priority
    PRIORITY_OTHERS = 1.0           # Lower priority
    
    def __init__(self, llm_analyzer: LLMAnalyzer):
        """Initialize evidence ranker."""
        self.llm_analyzer = llm_analyzer
    
    def _get_source_priority(self, url: str, source_type: str = None) -> float:
        """Determine priority level based on URL and source type."""
        url_lower = url.lower()
        
        # Priority 1: Fact Check API direct hits
        if source_type == "fact_check_api":
            return self.PRIORITY_FACT_CHECK_API
        
        # Check for fact-check domains (including Indian fact-checking sources)
        factcheck_domains = [
            "factcheck.org",
            "snopes.com",
            "politifact.com",
            "factchecker.in",
            "fullfact.org",
            "africacheck.org",
            "checkyourfact.com",
            "leadstories.com",
            "factcheck",
            "snopes",
            "politifact",
            # Indian fact-checking whitelist
            "altnews.in",
            "boomlive.in",
            "factly.in",
            "pib.gov.in",
            "indiatoday.in/fact-check",
            "thequint.com/fact-check",
            "factcrescendo.com"
        ]
        if any(domain in url_lower for domain in factcheck_domains):
            return self.PRIORITY_FACT_CHECK_API
        
        # Priority 2: Government sources
        gov_domains = [".gov", ".gov.uk", ".gov.au", ".gov.ca", ".europa.eu"]
        if any(url_lower.endswith(domain) or f"/{domain.split('.')[0]}" in url_lower for domain in gov_domains):
            return self.PRIORITY_GOV_EDU_NEWS
        
        # Priority 2: Educational sources
        edu_domains = [".edu", ".ac.uk", ".edu.au", ".ac.ca"]
        if any(url_lower.endswith(domain) or domain in url_lower for domain in edu_domains):
            return self.PRIORITY_GOV_EDU_NEWS
        
        # Priority 2: News sources (major news organizations)
        news_domains = [
            "reuters.com",
            "ap.org",
            "bbc.com",
            "bbc.co.uk",
            "nytimes.com",
            "washingtonpost.com",
            "theguardian.com",
            "wsj.com",
            "bloomberg.com",
            "cnn.com",
            "npr.org",
            "pbs.org"
        ]
        if any(domain in url_lower for domain in news_domains):
            return self.PRIORITY_GOV_EDU_NEWS
        
        # Priority 3: Others
        return self.PRIORITY_OTHERS
    
    def _is_authoritative_source(self, url: str) -> bool:
        """Check if URL is from an authoritative source."""
        priority = self._get_source_priority(url)
        return priority >= self.PRIORITY_GOV_EDU_NEWS
    
    def rank_by_relevance(
        self,
        claim: str,
        evidence_snippets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Rank evidence snippets by relevance and priority.
        
        Priority order:
        1. Fact Check API direct hits
        2. Gov/Edu/News authoritative sources
        3. Others
        """
        if not evidence_snippets:
            return []
        
        claim_lower = claim.lower()
        claim_words = set(claim_lower.split())
        
        scored_snippets = []
        for snippet in evidence_snippets:
            url = snippet.get("url", "")
            source_type = snippet.get("source", "")
            text = (snippet.get("snippet", "") or snippet.get("text", "") or "").lower()
            title = (snippet.get("title", "") or "").lower()
            
            # Calculate base relevance score
            relevance_score = 0.0
            
            # Title matches are more important
            if title:
                title_words = set(title.split())
                title_overlap = len(claim_words & title_words) / max(len(claim_words), 1)
                relevance_score += title_overlap * 0.4
            
            # Text matches
            if text:
                text_words = set(text.split())
                text_overlap = len(claim_words & text_words) / max(len(claim_words), 1)
                relevance_score += text_overlap * 0.3
            
            # Get source priority
            source_priority = self._get_source_priority(url, source_type)
            
            # Calculate final score: relevance * priority multiplier
            # Priority acts as a multiplier to boost authoritative sources
            final_score = relevance_score * source_priority
            
            # Add bonus for exact match types
            if source_priority == self.PRIORITY_FACT_CHECK_API:
                final_score += 0.5  # Bonus for fact-check API
            
            scored_snippets.append({
                **snippet,
                "relevance_score": relevance_score,
                "source_priority": source_priority,
                "final_score": final_score,
                "text": snippet.get("snippet", "") or snippet.get("text", ""),
                "is_authoritative": self._is_authoritative_source(url)
            })
        
        # Sort by final_score (descending) - this ensures priority AND relevance
        scored_snippets.sort(key=lambda x: x.get("final_score", 0.0), reverse=True)
        
        return scored_snippets
    
    async def summarize_evidence(
        self,
        claim: str,
        ranked_snippets: List[Dict[str, Any]],
        max_snippets: int = 10
    ) -> List[Dict[str, Any]]:
        """Summarize and select top evidence snippets."""
        # Prioritize: Fact Check API > Gov/Edu/News > Others
        fact_check_snippets = [s for s in ranked_snippets if s.get("source_priority") == self.PRIORITY_FACT_CHECK_API]
        authoritative_snippets = [s for s in ranked_snippets if s.get("source_priority") == self.PRIORITY_GOV_EDU_NEWS]
        other_snippets = [s for s in ranked_snippets if s.get("source_priority") == self.PRIORITY_OTHERS]
        
        # Build final list maintaining priority order
        top_snippets = []
        top_snippets.extend(fact_check_snippets[:5])  # Top 5 from Fact Check API
        remaining = max_snippets - len(top_snippets)
        top_snippets.extend(authoritative_snippets[:remaining])  # Fill with authoritative
        remaining = max_snippets - len(top_snippets)
        top_snippets.extend(other_snippets[:remaining])  # Fill with others
        
        return top_snippets[:max_snippets]
