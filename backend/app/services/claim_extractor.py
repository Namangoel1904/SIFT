"""Service for extracting claims from text."""
import re
from typing import List, Dict, Any
from ..services.utils import clean_text
from ..services.llm_analyzer import LLMAnalyzer


class ClaimExtractor:
    """Extract factual claims from text using LLM."""
    
    def __init__(self, llm_analyzer: LLMAnalyzer):
        """Initialize claim extractor."""
        self.llm_analyzer = llm_analyzer
    
    async def extract_claims(self, text: str) -> List[Dict[str, Any]]:
        """Extract factual claims from text."""
        if not text or len(text.strip()) < 10:
            return []
        
        # Clean text
        cleaned_text = clean_text(text)
        
        # Use LLM to extract claims
        prompt = f"""Analyze the following text and extract all factual claims that can be fact-checked.
        
        A claim is a statement that can be verified as true or false. Focus on:
        - Statistical statements
        - Historical facts
        - Scientific claims
        - Statements about events or people
        - Claims about dates, numbers, or specific facts
        
        Text to analyze:
        {cleaned_text}
        
        Return a JSON array of claims, each with:
        - "claim": the extracted claim text
        - "type": the type of claim (statistical, historical, scientific, event, etc.)
        - "confidence": confidence score (0-1)
        
        Format: {{"claims": [{{"claim": "...", "type": "...", "confidence": 0.9}}]}}"""
        
        try:
            response = await self.llm_analyzer.analyze(prompt, response_format="json")
            if isinstance(response, dict) and "claims" in response:
                return response["claims"]
            elif isinstance(response, list):
                return response
        except Exception as e:
            print(f"Error extracting claims: {e}")
        
        # Fallback: simple pattern-based extraction
        return self._extract_claims_fallback(cleaned_text)
    
    def _extract_claims_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback claim extraction using patterns."""
        claims = []
        
        # Patterns for common claim types
        patterns = {
            "statistical": [
                r'\d+%',
                r'\d+\s+(percent|percentage|million|billion)',
                r'(studies|research|data)\s+(show|indicate|suggest)',
            ],
            "historical": [
                r'(in|on|during)\s+\d{4}',
                r'(happened|occurred|took place)\s+(in|on)',
            ],
            "scientific": [
                r'(research|study|scientists)\s+(find|found|discover)',
                r'(proven|proves|evidence)\s+(that|shows)',
            ]
        }
        
        sentences = re.split(r'[.!?]\s+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            for claim_type, patterns_list in patterns.items():
                for pattern in patterns_list:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        claims.append({
                            "claim": sentence,
                            "type": claim_type,
                            "confidence": 0.5
                        })
                        break
        
        return claims[:10]  # Limit to top 10 claims

