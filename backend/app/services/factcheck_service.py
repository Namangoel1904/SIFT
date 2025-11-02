"""Main fact-checking service that orchestrates the workflow."""
import logging
from typing import List, Dict, Any
from ..services.claim_extractor import ClaimExtractor
from ..services.query_generator import QueryGenerator
from ..services.search_service import SearchService
from ..services.crawler import Crawler
from ..services.llm_analyzer import LLMAnalyzer
from ..services.evidence_ranker import EvidenceRanker
from ..services.language_service import LanguageService
from ..services.translation_service import TranslationService

logger = logging.getLogger(__name__)


class FactCheckService:
    """Main service for fact-checking content."""
    
    def __init__(self):
        """Initialize fact-check service."""
        self.llm_analyzer = LLMAnalyzer()
        self.claim_extractor = ClaimExtractor(self.llm_analyzer)
        self.query_generator = QueryGenerator(self.llm_analyzer)
        self.search_service = SearchService()
        self.crawler = Crawler()
        self.evidence_ranker = EvidenceRanker(self.llm_analyzer)
        self.language_service = LanguageService()
        self.translation_service = TranslationService()
    
    async def analyze_text(self, text: str, url: str = None) -> Dict[str, Any]:
        """Analyze text and fact-check claims.
        
        Workflow:
        1. extract_claims() - Extract factual claims from text
        2. build_search_queries() - Generate search queries for each claim
        3. call Fact Check Tools API - Search fact-checking sources
        4. call Custom Search API - Search general web
        5. crawl & extract useful text - Fetch and parse content
        6. summarize + rank evidence snippets - Rank by relevance
        7. LLM call (Gemini) - Generate structured JSON verdict
        
        Returns structured format:
        {
            "claims": [
                {
                    "claim": "...",
                    "verdict": "true|false|misleading|no_info",
                    "confidence": 0-1,
                    "explanation": "...",
                    "citations": ["https://..."]
                }
            ],
            "summary": "...",
            "methodology": "...",
            "limitations": "..."
        }
        """
        if not text or len(text.strip()) < 10:
            return {
                "claims": [],
                "summary": "No analyzable text found. Please select at least 10 characters.",
                "methodology": "SIFT uses AI-powered claim extraction and fact-checking against verified sources.",
                "limitations": "Analysis quality depends on available sources and may not cover all claims."
            }
        
        # Step 0: Detect language and translate to English BEFORE claim extraction
        original_text = text
        detected_language = self.language_service.detect_language(text)
        
        if detected_language != "en":
            logger.info(f"Detected non-English language: {detected_language}, translating to English before analysis")
            text = self.translation_service.translate_to_english(text)
            logger.info(f"Translation completed. Original length: {len(original_text)}, Translated length: {len(text)}")
        else:
            logger.debug("Text is already in English, no translation needed")
        
        # Step 1: Extract claims (from translated English text)
        claims = await self.claim_extractor.extract_claims(text)
        
        if not claims:
            return {
                "claims": [],
                "summary": "No factual claims detected in the selected text.",
                "methodology": "SIFT analyzes text for verifiable factual claims using AI.",
                "limitations": "Opinions, questions, and subjective statements may not be detected."
            }
        
        # Step 2: Fact-check each claim (already in English after translation)
        claim_results = []
        for claim_data in claims[:5]:  # Limit to top 5 claims
            claim_text = claim_data.get("claim", "")  # Already in English
            claim_type = claim_data.get("type", "general")
            
            # Step 3 & 4: Build search queries and call APIs
            queries = await self.query_generator.generate_queries(claim_text, claim_type)
            
            # Collect evidence from multiple sources
            all_evidence = []
            fact_check_has_results = False
            
            for query in queries[:3]:  # Use top 3 queries
                # Call Fact Check Tools API
                fact_check_results = await self.search_service.search_factcheck_api(query, 5)
                if fact_check_results:
                    fact_check_has_results = True
                all_evidence.extend(fact_check_results)
                
                # Call Custom Search API
                google_results = await self.search_service.search_google_custom(query, 5)
                all_evidence.extend(google_results)
            
            # Deduplicate by URL
            seen_urls = set()
            unique_evidence = []
            for item in all_evidence:
                url = item.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_evidence.append(item)
            
            # Step 5: Crawl and extract useful text from top sources
            crawled_evidence = []
            for source in unique_evidence[:10]:  # Limit crawling to top 10
                url = source.get("url", "")
                if url:
                    try:
                        crawled = await self.crawler.fetch_url(url)
                        if crawled:
                            # Enhance source with crawled content
                            source["crawled_text"] = crawled.get("text", "")[:1000]  # First 1000 chars
                            crawled_evidence.append(source)
                    except Exception as e:
                        logger.warning(f"Error crawling source {url}: {e}")
                        # Use snippet if available, continue analysis
                        crawled_evidence.append(source)
            
            # Use crawled evidence, fallback to original if crawling failed
            if not crawled_evidence:
                crawled_evidence = unique_evidence
            
            # Step 6: Summarize and rank evidence snippets
            ranked_evidence = self.evidence_ranker.rank_by_relevance(
                claim_text,
                crawled_evidence
            )
            
            top_evidence = await self.evidence_ranker.summarize_evidence(
                claim_text,
                ranked_evidence,
                max_snippets=10
            )
            
            # Extract citations
            citations = [e.get("url", "") for e in top_evidence if e.get("url")]
            
            # Step 7: LLM call (Gemini) - Generate structured JSON verdict
            factcheck_result = await self.llm_analyzer.factcheck_claim(
                claim_text,
                context=text[:500],  # First 500 chars as context (already in English)
                evidence_snippets=top_evidence
            )
            
            # Map verdict to required format
            verdict = factcheck_result.get("verdict", "unverified")
            verdict_mapping = {
                "true": "true",
                "false": "false",
                "partially_true": "misleading",
                "unverified": "no_info"
            }
            mapped_verdict = verdict_mapping.get(verdict, "no_info")
            
            # Adjust confidence based on Fact Check API results
            base_confidence = factcheck_result.get("confidence", 0.0)
            
            # If Fact Check API returned 403 or zero results, lower confidence slightly
            # But don't change verdict to "no_info" - let LLM decision stand
            if not fact_check_has_results and not citations:
                # No fact-check matches and no other sources - lower confidence by 10%
                adjusted_confidence = max(base_confidence * 0.9, 0.1)
            elif not fact_check_has_results:
                # No fact-check matches but we have other sources - lower confidence by 5%
                adjusted_confidence = max(base_confidence * 0.95, 0.1)
            else:
                # Fact Check API had results - use base confidence
                adjusted_confidence = base_confidence
            
            # Step 8: Generate AI-verified final verdict by analyzing ALL evidence
            # Separate evidence by type for final verdict
            factcheck_api_results = [e for e in unique_evidence if e.get("source") == "fact_check_api"]
            crawled_content_list = [e for e in crawled_evidence if e.get("crawled_text")]
            search_snippets_list = [e for e in all_evidence if e.get("source") == "google_custom_search" or (e.get("url") and not e.get("crawled_text"))]
            
            try:
                final_verdict = await self.llm_analyzer.generate_final_verdict(
                    claim_text,
                    factcheck_api_results,
                    crawled_content_list,
                    search_snippets_list
                )
                logger.info(f"Final verdict generated for claim: {claim_text[:50]}... Score: {final_verdict.get('score')}, Verdict: {final_verdict.get('verdict')}")
            except Exception as e:
                logger.warning(f"Final verdict generation failed for claim: {e}, using evidence-only result")
                final_verdict = {
                    "score": int(adjusted_confidence * 100),
                    "verdict": mapped_verdict.upper(),
                    "confidence": "medium",
                    "reasoning": factcheck_result.get("explanation", ""),
                    "citations": citations[:5]
                }
            
            # Build claim result with language information
            # Note: claim_text is already in English after translation
            claim_result = {
                "claim": claim_text,  # English claim (from translated text)
                "verdict": mapped_verdict,  # Keep LLM verdict, don't auto-change to "no_info"
                "confidence": round(adjusted_confidence, 2),
                "explanation": factcheck_result.get("explanation", ""),
                "citations": citations,
                "analysis_language": detected_language,  # Language of original input
                # Final AI-verified scoring
                "final_score": final_verdict.get("score", 50),
                "final_verdict": final_verdict.get("verdict", "UNCERTAIN"),
                "final_reasoning": final_verdict.get("reasoning", ""),
                "final_citations": final_verdict.get("citations", [])
            }
            
            # Add original claim if translation was performed
            if detected_language != "en":
                # Try to find corresponding original claim text
                # Since we translated the entire text, we need to map back
                # For now, we'll store the full original text context
                claim_result["original_claim"] = original_text  # Store full original text
                claim_result["claim_translated"] = claim_text  # English version
            else:
                claim_result["original_claim"] = claim_text  # Same for English
            
            claim_results.append(claim_result)
        
        # Generate summary text
        total = len(claim_results)
        true_count = sum(1 for c in claim_results if c["verdict"] == "true")
        false_count = sum(1 for c in claim_results if c["verdict"] == "false")
        misleading_count = sum(1 for c in claim_results if c["verdict"] == "misleading")
        no_info_count = sum(1 for c in claim_results if c["verdict"] == "no_info")
        
        summary_parts = []
        if total > 0:
            summary_parts.append(f"Analyzed {total} claim{'s' if total != 1 else ''}")
            if true_count > 0:
                summary_parts.append(f"{true_count} verified as true")
            if false_count > 0:
                summary_parts.append(f"{false_count} verified as false")
            if misleading_count > 0:
                summary_parts.append(f"{misleading_count} found to be misleading")
            if no_info_count > 0:
                summary_parts.append(f"{no_info_count} could not be verified")
        else:
            summary_parts.append("No claims analyzed")
        
        summary_text = ". ".join(summary_parts) + "."
        
        result = {
            "claims": claim_results,
            "summary": summary_text,
            "methodology": "SIFT uses Gemini 2.0 Flash to extract factual claims from text, searches verified fact-checking sources via Fact Check Tools API and Google Custom Search, crawls source content, ranks evidence by relevance, and uses Gemini to provide verdicts with confidence scores. Citations link to original fact-check articles and sources.",
            "limitations": "Fact-checking accuracy depends on: (1) availability of relevant sources in Fact Check Tools API and search results, (2) recency of information (new claims may lack verification), (3) AI interpretation quality (Gemini model limitations), and (4) source reliability. Always review citations for complete context. Some claims may require expert review."
        }
        
        # Add language information at top level
        if detected_language != "en":
            result["original_text"] = original_text
            result["translated_text"] = text
            result["detected_language"] = detected_language
        
        return result
    
    async def factcheck_url(self, url: str) -> Dict[str, Any]:
        """Fact-check content from a URL.
        
        Fetches content from URL (supports HTML and PDF), extracts text,
        and runs the same fact-checking pipeline as text analysis.
        
        Returns the same format as analyze_text:
        {
            "claims": [...],
            "summary": "...",
            "methodology": "...",
            "limitations": "..."
        }
        """
        # Fetch URL content (includes PDF support via crawler)
        content = await self.crawler.fetch_url(url)
        
        if not content:
            return {
                "claims": [],
                "summary": "Could not fetch URL content. Please check if the URL is accessible and try again.",
                "methodology": "SIFT uses Gemini 2.0 Flash to extract factual claims from text, searches verified fact-checking sources via Fact Check Tools API and Google Custom Search, crawls source content, ranks evidence by relevance, and uses Gemini to provide verdicts with confidence scores. Citations link to original fact-check articles and sources.",
                "limitations": "Fact-checking accuracy depends on: (1) availability of relevant sources in Fact Check Tools API and search results, (2) recency of information (new claims may lack verification), (3) AI interpretation quality (Gemini model limitations), and (4) source reliability. Always review citations for complete context. Some claims may require expert review."
            }
        
        # Extract text from content (supports both HTML and PDF)
        text = content.get("text", "")
        if not text or len(text.strip()) < 10:
            return {
                "claims": [],
                "summary": "No analyzable text content found in URL. The page may be empty, contain only images, or be inaccessible.",
                "methodology": "SIFT uses Gemini 2.0 Flash to extract factual claims from text, searches verified fact-checking sources via Fact Check Tools API and Google Custom Search, crawls source content, ranks evidence by relevance, and uses Gemini to provide verdicts with confidence scores. Citations link to original fact-check articles and sources.",
                "limitations": "Fact-checking accuracy depends on: (1) availability of relevant sources in Fact Check Tools API and search results, (2) recency of information (new claims may lack verification), (3) AI interpretation quality (Gemini model limitations), and (4) source reliability. Always review citations for complete context. Some claims may require expert review."
            }
        
        # Use analyze_text pipeline (same as /analyze endpoint)
        result = await self.analyze_text(text, url)
        
        # Add URL metadata if available
        if content.get("title"):
            result["source_title"] = content.get("title", "")
        if content.get("description"):
            result["source_description"] = content.get("description", "")
        
        return result
