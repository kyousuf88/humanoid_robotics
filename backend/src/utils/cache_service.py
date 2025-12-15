import asyncio
import hashlib
import json
from typing import Optional, Dict, Any, Union
from datetime import datetime, timedelta
from collections import OrderedDict
from src.utils.logger import logger
from src.utils.config import settings


class LRUCache:
    """
    Simple LRU (Least Recently Used) cache implementation.
    """

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):  # 1 hour default TTL
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.ttl_cache = {}  # Track expiration times

    def _cleanup_expired(self):
        """Remove expired entries from the cache."""
        current_time = datetime.utcnow().timestamp()
        expired_keys = [key for key, expiry in self.ttl_cache.items() if current_time > expiry]

        for key in expired_keys:
            if key in self.cache:
                del self.cache[key]
            if key in self.ttl_cache:
                del self.ttl_cache[key]

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        self._cleanup_expired()

        if key not in self.cache:
            return None

        # Move to end (most recently used)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key: str, value: Any, ttl: Optional[int] = None):
        """Put a value in the cache with optional TTL."""
        self._cleanup_expired()

        if ttl is None:
            ttl = self.default_ttl

        expiry_time = datetime.utcnow().timestamp() + ttl

        if key in self.cache:
            # Update existing key
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used item
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            self.ttl_cache.pop(oldest_key, None)

        self.cache[key] = value
        self.ttl_cache[key] = expiry_time

    def delete(self, key: str):
        """Delete a key from the cache."""
        if key in self.cache:
            del self.cache[key]
        if key in self.ttl_cache:
            del self.ttl_cache[key]

    def clear(self):
        """Clear all entries from the cache."""
        self.cache.clear()
        self.ttl_cache.clear()

    def size(self) -> int:
        """Get the current size of the cache."""
        self._cleanup_expired()
        return len(self.cache)


class CacheService:
    """
    Service for caching frequently asked questions and other data to improve performance.
    """

    def __init__(self):
        # Initialize LRU cache with configurable size
        cache_size = int(getattr(settings, 'cache_size', 1000))
        default_ttl = int(getattr(settings, 'cache_default_ttl', 3600))  # 1 hour

        self.cache = LRUCache(max_size=cache_size, default_ttl=default_ttl)
        self.is_enabled = getattr(settings, 'cache_enabled', True)

    def _generate_cache_key(self, question: str, context_mode: str, selected_text: Optional[str] = None) -> str:
        """
        Generate a unique cache key for a question.

        Args:
            question: The question text
            context_mode: The context mode ('full_book' or 'selected_text')
            selected_text: Optional selected text

        Returns:
            Hashed cache key string
        """
        cache_input = {
            'question': question.strip().lower(),
            'context_mode': context_mode,
            'selected_text': selected_text.strip().lower() if selected_text else None
        }

        # Create a hash of the input to use as cache key
        cache_input_str = json.dumps(cache_input, sort_keys=True)
        cache_key = hashlib.sha256(cache_input_str.encode()).hexdigest()

        return f"qa:{cache_key}"

    def get_cached_response(self, question: str, context_mode: str = "full_book",
                           selected_text: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get a cached response for a question if it exists.

        Args:
            question: The question text
            context_mode: The context mode ('full_book' or 'selected_text')
            selected_text: Optional selected text

        Returns:
            Cached response or None if not found/cached
        """
        if not self.is_enabled:
            return None

        cache_key = self._generate_cache_key(question, context_mode, selected_text)
        cached_data = self.cache.get(cache_key)

        if cached_data:
            logger.info("Cache hit for question", extra={
                "cache_key": cache_key,
                "question_length": len(question)
            })
            return cached_data

        logger.debug("Cache miss for question", extra={
            "cache_key": cache_key,
            "question_length": len(question)
        })
        return None

    def cache_response(self, question: str, context_mode: str, response: Dict[str, Any],
                      selected_text: Optional[str] = None, ttl: Optional[int] = None):
        """
        Cache a response for a question.

        Args:
            question: The question text
            context_mode: The context mode ('full_book' or 'selected_text')
            response: The response to cache
            selected_text: Optional selected text
            ttl: Time-to-live in seconds (optional, uses default if not provided)
        """
        if not self.is_enabled:
            return

        cache_key = self._generate_cache_key(question, context_mode, selected_text)

        # Add cache timestamp to the response
        cached_response = {
            **response,
            "cached_at": datetime.utcnow().isoformat(),
            "cache_hit": False  # This will be set to True when retrieved from cache
        }

        self.cache.put(cache_key, cached_response, ttl)

        logger.info("Cached response for question", extra={
            "cache_key": cache_key,
            "question_length": len(question),
            "ttl": ttl or self.cache.default_ttl
        })

    def invalidate_question(self, question: str, context_mode: str = "full_book",
                           selected_text: Optional[str] = None):
        """
        Invalidate (remove) a cached response for a question.

        Args:
            question: The question text
            context_mode: The context mode ('full_book' or 'selected_text')
            selected_text: Optional selected text
        """
        cache_key = self._generate_cache_key(question, context_mode, selected_text)
        self.cache.delete(cache_key)

        logger.info("Invalidated cache for question", extra={
            "cache_key": cache_key,
            "question_length": len(question)
        })

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "enabled": self.is_enabled,
            "size": self.cache.size(),
            "max_size": self.cache.max_size,
            "default_ttl": self.cache.default_ttl
        }

    def clear_cache(self):
        """Clear all cached data."""
        self.cache.clear()
        logger.info("Cleared entire cache")


# Global cache service instance
cache_service = CacheService()