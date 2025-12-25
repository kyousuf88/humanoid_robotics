from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class SourceCitation(BaseModel):
    """Represents a citation to a source in the book"""
    url: str
    title: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)


class QueryResult(BaseModel):
    """
    Contains the answer to a user's question along with source citations
    and relevance scores; returned to the frontend.
    """
    id: UUID = Field(default_factory=uuid4)
    question: str = Field(..., min_length=1, max_length=5000)
    answer: str = Field(..., min_length=1, max_length=10000)
    source_citations: List[SourceCitation] = Field(..., min_items=1)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    retrieved_chunks: Optional[List[UUID]] = Field(default=None)  # References to BookChunk IDs
    query_timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[UUID] = Field(default=None)

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }