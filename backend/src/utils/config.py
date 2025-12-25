from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # API Keys
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")

    # Database URLs
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # Application Settings
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Rate Limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # in seconds

    # Model settings
    cohere_model: str = os.getenv("COHERE_MODEL", "embed-multilingual-v3.0")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Performance settings
    response_timeout: int = int(os.getenv("RESPONSE_TIMEOUT", "30"))  # seconds
    max_query_length: int = int(os.getenv("MAX_QUERY_LENGTH", "1000"))  # characters
    max_selected_text_length: int = int(os.getenv("MAX_SELECTED_TEXT_LENGTH", "5000"))  # characters

    # Language settings
    book_language: str = os.getenv("BOOK_LANGUAGE", "en")  # Default to English

    # Cache settings
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    cache_size: int = int(os.getenv("CACHE_SIZE", "1000"))
    cache_default_ttl: int = int(os.getenv("CACHE_DEFAULT_TTL", "3600"))  # 1 hour in seconds

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Create a global settings instance
settings = get_settings()