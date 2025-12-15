from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class UserSession(BaseModel):
    """
    Tracks the context of a user's interaction, particularly for selected-text questions
    that need to maintain focus on specific content.
    """
    id: UUID = Field(default_factory=uuid4)
    session_token: str = Field(..., min_length=10, max_length=255)  # Unique token for rate limiting
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    selected_text: Optional[str] = Field(default=None, max_length=5000)  # Max 1000 words/tokens
    query_history: List[UUID] = Field(default_factory=list)  # References to QueryResult IDs
    rate_limit_remaining: int = Field(default=100, ge=0)  # Remaining requests in current window
    rate_limit_reset: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=1))
    context_preservation: Optional[dict] = Field(default=None)  # For maintaining context across follow-up questions

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }

    def is_expired(self) -> bool:
        """Check if session has expired due to inactivity (30 minutes)"""
        return (datetime.utcnow() - self.last_activity).total_seconds() > 1800  # 30 minutes

    def is_rate_limited(self) -> bool:
        """Check if session has exceeded rate limit"""
        return self.rate_limit_remaining <= 0

    def update_selected_text(self, text: Optional[str]) -> None:
        """Update the selected text in the session"""
        self.selected_text = text
        self.last_activity = datetime.utcnow()

    def preserve_context(self, context_data: dict) -> None:
        """Preserve context data for follow-up questions"""
        self.context_preservation = context_data
        self.last_activity = datetime.utcnow()