"""Service for language detection only."""
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import logging

logger = logging.getLogger(__name__)


class LanguageService:
    """Service for detecting the language of text."""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Language code (e.g., "en", "hi", "bn") or "en" as fallback
        """
        if not text or len(text.strip()) < 3:
            return "en"
        
        try:
            detected = detect(text)
            logger.debug(f"Detected language: {detected} for text: {text[:50]}")
            return detected
        except LangDetectException as e:
            logger.debug(f"Language detection failed: {e}, defaulting to 'en'")
            return "en"
        except Exception as e:
            logger.warning(f"Unexpected error in language detection: {e}, defaulting to 'en'")
            return "en"
