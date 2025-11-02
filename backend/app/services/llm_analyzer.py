"""Service for LLM-based analysis using Google Gemini."""
import httpx
import json
from typing import Dict, Any, Optional, List
from ..config import settings


SYSTEM_PROMPT = """You are a fact-checking assistant. Your task is to analyze claims and provide structured JSON responses only.

You must respond with valid JSON only. Do not include any markdown formatting, code blocks, or explanatory text outside the JSON.

When fact-checking:
- "true": Claim is verified as factually correct
- "false": Claim is verified as factually incorrect
- "partially_true": Claim is misleading or partially true
- "unverified": Cannot determine with available information

Always return confidence scores between 0.0 and 1.0."""


class LLMAnalyzer:
    """Analyzer using Google Gemini API."""
    
    def __init__(self):
        """Initialize LLM analyzer."""
        self.api_key = settings.GOOGLE_API_KEY
        self.model = settings.SIFT_GEMINI_MODEL
        self.endpoint_base = settings.GEMINI_ENDPOINT
        self.temperature = settings.GEMINI_TEMPERATURE
    
    def _get_endpoint_url(self) -> str:
        """Get the Gemini API endpoint URL."""
        return f"{self.endpoint_base}/{self.model}:generateContent"
    
    async def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
        temperature: Optional[float] = None
    ) -> Any:
        """Analyze text using Gemini API."""
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not configured")
        
        system_message = system_prompt or SYSTEM_PROMPT
        
        # Gemini API structure
        contents = [
            {
                "role": "user",
                "parts": [
                    {"text": system_message},
                    {"text": prompt}
                ]
            }
        ]
        
        generation_config = {
            "temperature": temperature or self.temperature,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
        }
        
        if response_format == "json":
            generation_config["responseMimeType"] = "application/json"
        
        payload = {
            "contents": contents,
            "generationConfig": generation_config
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = self._get_endpoint_url()
                params = {"key": self.api_key}
                
                response = await client.post(
                    url,
                    json=payload,
                    params=params
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract text from Gemini response
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            content = parts[0]["text"]
                            
                            # Parse JSON if requested
                            if response_format == "json":
                                try:
                                    return json.loads(content)
                                except json.JSONDecodeError:
                                    # Try to extract JSON from markdown code blocks
                                    import re
                                    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                                    if json_match:
                                        return json.loads(json_match.group(1))
                                    # Try bare JSON
                                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                                    if json_match:
                                        return json.loads(json_match.group())
                                    return {"error": "Could not parse JSON response", "raw": content}
                            
                            return content
                
                raise ValueError("Unexpected response format from Gemini API")
        
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error in Gemini API: {e.response.status_code}"
            if e.response.text:
                error_msg += f" - {e.response.text}"
            print(error_msg)
            raise
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            raise
    
    async def factcheck_claim(
        self,
        claim: str,
        context: Optional[str] = None,
        evidence_snippets: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Fact-check a claim using Gemini with evidence snippets.
        
        Includes URL + snippet for each evidence piece in the prompt.
        """
        evidence_text = ""
        if evidence_snippets:
            evidence_text = "\n\nEvidence Snippets (ranked by relevance and source authority):\n"
            for i, snippet in enumerate(evidence_snippets[:10], 1):
                source = snippet.get("source", "Unknown")
                text = snippet.get("text", "") or snippet.get("snippet", "")
                url = snippet.get("url", "")
                relevance_score = snippet.get("relevance_score", 0.0)
                source_priority = snippet.get("source_priority", 1.0)
                is_authoritative = snippet.get("is_authoritative", False)
                
                # Priority indicator
                priority_label = ""
                if source_priority >= 3.0:
                    priority_label = " [FACT-CHECK API - Highest Priority]"
                elif source_priority >= 2.0:
                    priority_label = " [Authoritative Source - Gov/Edu/News]"
                
                evidence_text += f"{i}. Source: {source}{priority_label}\n"
                evidence_text += f"   URL: {url}\n"
                evidence_text += f"   Snippet: {text[:400]}\n"
                evidence_text += f"   Relevance Score: {relevance_score:.2f}\n\n"
        
        context_text = f"\nOriginal Context: {context[:500]}" if context else ""
        
        prompt = f"""Fact-check the following claim based on the provided evidence snippets.

Claim: "{claim}"{context_text}{evidence_text}

Analyze the evidence considering:
- Fact Check API sources are highest priority
- Government, educational, and major news sources are authoritative
- URL credibility and snippet relevance

Provide a JSON object with:
{{
    "verdict": "true|false|partially_true|unverified",
    "confidence": 0.0-1.0,
    "explanation": "A clear 2-3 sentence explanation of your verdict, referencing specific URLs and snippets",
    "evidence": "Key supporting evidence from the snippets, include URL references where relevant"
}}

Return ONLY valid JSON, no markdown, no code blocks."""
        
        try:
            response = await self.analyze(prompt, response_format="json", temperature=self.temperature)
            if isinstance(response, dict):
                return {
                    "verdict": response.get("verdict", "unverified"),
                    "confidence": float(response.get("confidence", 0.0)),
                    "explanation": response.get("explanation", ""),
                    "evidence": response.get("evidence", "")
                }
        except Exception as e:
            print(f"Error in fact-checking: {e}")
        
        # Fallback response
        return {
            "verdict": "unverified",
            "confidence": 0.0,
            "explanation": "Could not verify claim due to analysis error.",
            "evidence": ""
        }
    
    async def generate_final_verdict(
        self,
        claim: str,
        factcheck_results: List[Dict[str, Any]],
        crawled_content: List[Dict[str, Any]],
        search_snippets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate final AI-verified verdict by analyzing all evidence sources.
        
        Weighs FactCheck API results highest, evaluates domain authority,
        and computes a comprehensive truth score (0-100).
        
        Args:
            claim: The claim to verify
            factcheck_results: List of FactCheck API results
            crawled_content: List of crawled article excerpts
            search_snippets: List of search result snippets
            
        Returns:
            Dict with score (0-100), verdict, confidence, reasoning, and citations
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # Build comprehensive evidence summary
        evidence_text = "=== EVIDENCE SUMMARY ===\n\n"
        
        # FactCheck API results (highest priority)
        if factcheck_results:
            evidence_text += "FACT-CHECK API RESULTS (Highest Priority):\n"
            for i, result in enumerate(factcheck_results[:5], 1):
                url = result.get("url", "")
                snippet = result.get("snippet", "")
                title = result.get("title", "")
                evidence_text += f"{i}. {title}\n"
                evidence_text += f"   URL: {url}\n"
                evidence_text += f"   Content: {snippet[:300]}\n\n"
        
        # Crawled content (authoritative sources)
        if crawled_content:
            evidence_text += "\nCRAWLED ARTICLE CONTENT:\n"
            for i, content in enumerate(crawled_content[:5], 1):
                url = content.get("url", "")
                text = content.get("crawled_text", "") or content.get("text", "")
                title = content.get("title", "")
                domain = url.split("/")[2] if url else "unknown"
                evidence_text += f"{i}. {title} ({domain})\n"
                evidence_text += f"   URL: {url}\n"
                evidence_text += f"   Excerpt: {text[:400]}\n\n"
        
        # Search snippets
        if search_snippets:
            evidence_text += "\nSEARCH RESULT SNIPPETS:\n"
            for i, snippet in enumerate(search_snippets[:5], 1):
                url = snippet.get("url", "")
                text = snippet.get("snippet", "")
                title = snippet.get("title", "")
                domain = url.split("/")[2] if url else "unknown"
                evidence_text += f"{i}. {title} ({domain})\n"
                evidence_text += f"   URL: {url}\n"
                evidence_text += f"   Snippet: {text[:300]}\n\n"
        
        if not evidence_text or evidence_text == "=== EVIDENCE SUMMARY ===\n\n":
            evidence_text = "No evidence found from any sources."
        
        prompt = f"""Analyze ALL provided evidence to generate a FINAL VERDICT for this claim.

CLAIM: "{claim}"

{evidence_text}

INSTRUCTIONS:
1. Analyze supporting vs contradicting sources
2. Weigh FactCheck API results HIGHEST (they are verified fact-checks)
3. Evaluate domain authority: .gov, .edu, major news outlets (Reuters, BBC, etc.) are more credible
4. Consider recency and source diversity
5. Compute a TRUTH SCORE (0-100 integer) where:
   - 90-100: TRUE (strong evidence from multiple authoritative sources)
   - 70-89: LIKELY TRUE (good evidence, may have minor contradictions)
   - 40-69: UNCERTAIN / MIXED (conflicting evidence or insufficient data)
   - 20-39: LIKELY FALSE (evidence suggests falsehood, but not definitive)
   - 0-19: FALSE (strong evidence contradicts the claim)

6. Assign verdict label: TRUE, LIKELY_TRUE, UNCERTAIN, LIKELY_FALSE, or FALSE
7. Provide confidence level: "high", "medium", or "low"
8. Write 3-5 sentence reasoning explaining your score, mentioning specific sources
9. List key citation URLs (up to 5 most important)

Return JSON only:
{{
  "score": 85,
  "verdict": "LIKELY_TRUE",
  "confidence": "high",
  "reasoning": "Detailed reasoning here...",
  "citations": ["https://example1.com", "https://example2.com"]
}}

Return ONLY valid JSON, no markdown, no code blocks."""
        
        try:
            logger.info(f"Generating final verdict using {self.model} for claim: {claim[:50]}...")
            response = await self.analyze(prompt, response_format="json", temperature=0.1)
            
            if isinstance(response, dict):
                # Validate and normalize response
                score = int(response.get("score", 50))
                score = max(0, min(100, score))  # Clamp to 0-100
                
                verdict_raw = response.get("verdict", "UNCERTAIN").upper()
                verdict_map = {
                    "TRUE": "TRUE",
                    "LIKELY_TRUE": "LIKELY_TRUE",
                    "UNCERTAIN": "UNCERTAIN",
                    "MIXED": "UNCERTAIN",
                    "LIKELY_FALSE": "LIKELY_FALSE",
                    "FALSE": "FALSE"
                }
                verdict = verdict_map.get(verdict_raw, "UNCERTAIN")
                
                confidence_raw = response.get("confidence", "medium").lower()
                confidence_map = {"high": "high", "medium": "medium", "low": "low"}
                confidence = confidence_map.get(confidence_raw, "medium")
                
                reasoning = response.get("reasoning", "")
                citations = response.get("citations", [])
                if not isinstance(citations, list):
                    citations = []
                
                logger.info(f"Final verdict generated: {verdict} (score: {score}, confidence: {confidence})")
                
                return {
                    "score": score,
                    "verdict": verdict,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "citations": citations[:5]  # Limit to 5 citations
                }
            else:
                logger.warning(f"Unexpected response format from final verdict generation")
                return self._get_fallback_final_verdict()
                
        except Exception as e:
            logger.error(f"Error generating final verdict using {self.model}: {e}")
            return self._get_fallback_final_verdict()
    
    def _get_fallback_final_verdict(self) -> Dict[str, Any]:
        """Fallback final verdict when Gemini scoring fails."""
        return {
            "score": 50,
            "verdict": "UNCERTAIN",
            "confidence": "low",
            "reasoning": "Could not generate AI-verified final verdict. Showing evidence-only result.",
            "citations": []
        }
