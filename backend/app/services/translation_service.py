"""Service for translation using Google Cloud Translation API."""
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import logging
import hashlib
import json
import os

logger = logging.getLogger(__name__)


# Global cache for translations (works across instances)
_translation_cache = {}


class TranslationService:
    """Service for translating text to English using Google Cloud Translation API."""
    
    def __init__(self):
        """Initialize translation service.
        
        Supports both file-based credentials (GOOGLE_APPLICATION_CREDENTIALS)
        and JSON string credentials (GOOGLE_CREDENTIALS_JSON) for Render deployment.
        """
        try:
            # Try to initialize credentials from JSON string first (Render-compatible)
            credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            if credentials_json:
                try:
                    credentials_dict = json.loads(credentials_json)
                    credentials = service_account.Credentials.from_service_account_info(
                        credentials_dict
                    )
                    self.client = translate.Client(credentials=credentials)
                    self.enabled = True
                    logger.info("Translation Service initialized with JSON credentials (Render-compatible)")
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"Failed to parse GOOGLE_CREDENTIALS_JSON: {e}")
                    raise
            else:
                # Fallback to file-based credentials (local development)
                self.client = translate.Client()
                self.enabled = True
                logger.info("Translation Service initialized with file-based credentials")
        except Exception as e:
            logger.error(f"Translation Service init error: {e}")
            logger.warning("Translation will fallback to original text if translation is unavailable")
            self.client = None
            self.enabled = False
    
    def translate_to_english(self, text: str) -> str:
        """Translate text (detected language) → English using Google Cloud Translation API.
        
        Uses in-memory cache to avoid translating the same text multiple times.
        
        Args:
            text: Text to translate to English
            
        Returns:
            Translated text in English, or original text if translation fails
        """
        if not self.enabled or not text or len(text.strip()) < 3:
            return text  # Fallback: return original
        
        # Check cache first (use hash for key to handle long texts)
        cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()
        if cache_key in _translation_cache:
            logger.debug(f"Translation cache hit for text: {text[:50]}...")
            return _translation_cache[cache_key]
        
        try:
            result = self.client.translate(text, target_language="en")
            translated_text = result.get("translatedText", text)
            
            # Validate translation
            if translated_text and len(translated_text.strip()) > 0:
                # Store in cache (limit cache size to 200 entries)
                if len(_translation_cache) >= 200:
                    # Remove oldest entry (simple FIFO for now)
                    _translation_cache.pop(next(iter(_translation_cache)))
                
                _translation_cache[cache_key] = translated_text
                logger.debug(f"Translated '{text[:50]}...' to: '{translated_text[:50]}...'")
                return translated_text
            else:
                logger.warning(f"Translation returned empty text, using original")
                return text
                
        except Exception as e:
            logger.error(f"Translation API error: {e}")
            return text  # Fail gracefully - return original text

