from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class BookChunk(BaseModel):
    """
    Represents a segment of book content with text, source URL, chapter reference,
    and position in the book; used for embedding and retrieval.
    """
    id: UUID = Field(default_factory=uuid4)
    text_content: str = Field(..., min_length=1, max_length=10000)  # Max 10000 chars to allow for longer chunks
    source_url: str = Field(..., max_length=2048)
    chapter: str = Field(..., min_length=1, max_length=255)
    position: int = Field(..., ge=1)  # Must be positive integer
    embedding: Optional[list] = Field(default=None)  # Vector embedding as list of floats
    metadata: Optional[dict] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('source_url')
    def validate_source_url(cls, v):
        """Validate that source_url is a proper URL format"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('source_url must start with http:// or https://')
        return v

    @validator('text_content')
    def validate_text_content(cls, v):
        """Validate text content meets token requirements (200-800 tokens approximately)"""
        # For simplicity, we'll approximate tokens as words (in reality, 1 token ≈ 0.75 words)
        word_count = len(v.split())
        if word_count < 50:  # Approximate 200 tokens minimum
            raise ValueError('text_content is too short (minimum ~200 tokens)')
        if word_count > 1200:  # Approximate 800 tokens maximum
            raise ValueError('text_content is too long (maximum ~800 tokens)')
        return v

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }