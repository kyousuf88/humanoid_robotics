from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import time
import html
from src.utils.monitoring_service import monitoring_service

router = APIRouter()


class SessionInitRequest(BaseModel):
    """Request model for initializing a new session"""
    session_context: Optional[str] = Field(
        default=None,
        description="Optional context for the session, such as selected text or previous conversation context",
        example="The user has selected a paragraph about AI safety principles for focused questioning"
    )


class SessionInitResponse(BaseModel):
    """Response model for session initialization"""
    session_id: str
    rate_limit_remaining: int
    rate_limit_reset: str


@router.post(
    "/session/init",
    summary="Initialize User Session",
    description="Initialize a new user session with rate limiting and context preservation capabilities.",
    responses={
        200: {
            "description": "Successfully initialized a new session with rate limiting parameters",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "session_id": "550e8400-e29b-41d4-a716-446655440000",
                            "rate_limit_remaining": 100,
                            "rate_limit_reset": "2023-12-11T11:30:00.123456Z"
                        },
                        "request_id": "677e2553-ddc3-49e2-8e40-28a3b4e53b7f"
                    }
                }
            }
        }
    }
)
async def init_session(request: SessionInitRequest) -> Dict[str, Any]:
    """
    Initialize a new user session with rate limiting parameters.
    Creates a new session with appropriate rate limiting values.

    This endpoint establishes a new user session that includes:
    - A unique session identifier
    - Rate limiting parameters (100 requests per hour)
    - Optional session context for preserving conversation state
    """
    start_time = time.time()

    # Sanitize session context input
    sanitized_context = html.escape(request.session_context) if request.session_context else None

    # Generate a new session ID
    session_id = str(uuid.uuid4())

    # Set rate limiting parameters (100 requests per hour as per requirements)
    rate_limit_remaining = 100
    rate_limit_reset = datetime.utcnow() + timedelta(hours=1)

    response_time = (time.time() - start_time) * 1000
    monitoring_service.record_request("/v1/session/init", response_time, 200)

    return {
        "success": True,
        "data": {
            "session_id": session_id,
            "rate_limit_remaining": rate_limit_remaining,
            "rate_limit_reset": rate_limit_reset.isoformat()
        },
        "request_id": str(uuid.uuid4())
    }