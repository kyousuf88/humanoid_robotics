from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from src.services.chat_service import ChatService
from src.services.retrieval_service import RetrievalService
from src.models.query_result import QueryResult
from datetime import datetime
import uuid
import time
import html
from src.utils.monitoring_service import monitoring_service

router = APIRouter()
chat_service = ChatService()
retrieval_service = RetrievalService()


class ChatRequest(BaseModel):
    """Request model for the chat endpoint"""
    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The user's question about the book content",
        example="What are the key principles of AI safety discussed in this book?"
    )
    context_mode: str = Field(
        "full_book",
        pattern="^(full_book|selected_text)$",
        description="The context mode for answering. 'full_book' searches across the entire book, 'selected_text' focuses on user-selected text",
        example="full_book"
    )
    selected_text: Optional[str] = Field(
        None,
        max_length=5000,
        description="Text selected by user for focused questions (max 1000 words)",
        example="Artificial intelligence safety is a crucial field that focuses on ensuring AI systems behave as intended and do not cause harm."
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session identifier to maintain conversation context",
        example="550e8400-e29b-41d4-a716-446655440000"
    )


class ChatResponse(BaseModel):
    """Response model for the chat endpoint"""
    success: bool = Field(..., description="Indicates if the request was successful")
    data: Dict[str, Any] = Field(..., description="The response data containing answer and citations")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the response")
    request_id: str = Field(..., description="Unique identifier for the request")


@router.post(
    "/chat",
    summary="Chat with the RAG Bot",
    description="Process a user's question and return an AI-generated answer with source citations from the book content.",
    responses={
        200: {
            "description": "Successful response with AI-generated answer and citations",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "answer": "The key principles of AI safety include robustness, transparency, and value alignment...",
                            "source_citations": [
                                {
                                    "url": "https://example.com/chapter1",
                                    "title": "Chapter: Introduction to AI Safety",
                                    "relevance_score": 0.89
                                }
                            ],
                            "relevance_score": 0.85,
                            "session_id": "550e8400-e29b-41d4-a716-446655440000"
                        },
                        "timestamp": "2023-12-11T10:30:00.123456Z",
                        "request_id": "677e2553-ddc3-49e2-8e40-28a3b4e53b7f"
                    }
                }
            }
        },
        400: {
            "description": "Bad request - invalid input parameters",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "INVALID_INPUT",
                            "message": "selected_text is required when context_mode is 'selected_text'"
                        }
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "CHAT_GENERATION_FAILED",
                            "message": "Failed to generate chat response: [error details]"
                        }
                    }
                }
            }
        }
    }
)
async def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Process a user's question and return an AI-generated answer with source citations from the book content.

    This endpoint uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on the book content.
    It supports two context modes:
    - full_book: Searches across the entire book content
    - selected_text: Focuses on user-selected text passages

    The response includes source citations to allow users to verify the information.
    """
    start_time = time.time()

    # Sanitize inputs to prevent prompt injection
    sanitized_question = html.escape(request.question) if request.question else ""
    sanitized_selected_text = html.escape(request.selected_text) if request.selected_text else None

    # Validate request based on context_mode
    if request.context_mode == "selected_text":
        if not sanitized_selected_text:
            monitoring_service.record_request("/v1/chat", (time.time() - start_time) * 1000, 400)
            raise HTTPException(
                status_code=400,
                detail={
                    "error": {
                        "code": "INVALID_INPUT",
                        "message": "selected_text is required when context_mode is 'selected_text'"
                    }
                }
            )

        # Check if selected_text exceeds length limit (approximately 1000 words)
        if sanitized_selected_text and len(sanitized_selected_text.split()) > 1000:
            monitoring_service.record_request("/v1/chat", (time.time() - start_time) * 1000, 400)
            raise HTTPException(
                status_code=400,
                detail={
                    "error": {
                        "code": "INVALID_INPUT",
                        "message": "selected_text exceeds maximum length of 1000 words"
                    }
                }
            )

    try:
        # Generate the answer using the chat service with sanitized inputs
        query_result = chat_service.generate_answer(
            question=sanitized_question,
            context_mode=request.context_mode,
            selected_text=sanitized_selected_text
        )

        # Generate or use provided session ID
        session_id = request.session_id or str(uuid.uuid4())

        response_time = (time.time() - start_time) * 1000
        monitoring_service.record_request("/v1/chat", response_time, 200)

        return {
            "success": True,
            "data": {
                "answer": query_result.answer,
                "source_citations": [
                    {
                        "url": citation.url,
                        "title": citation.title,
                        "relevance_score": citation.relevance_score
                    }
                    for citation in query_result.source_citations
                ],
                "relevance_score": query_result.relevance_score,
                "session_id": session_id
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        monitoring_service.record_request("/v1/chat", response_time, 500)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "CHAT_GENERATION_FAILED",
                    "message": f"Failed to generate chat response: {str(e)}"
                }
            }
        )


@router.post(
    "/query",
    summary="Direct Vector Database Query",
    description="Query the vector database directly and return relevant chunks without AI processing.",
    responses={
        200: {
            "description": "Successful response with relevant text chunks from the vector database",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "query": "What are the key principles of AI safety?",
                            "results": [
                                {
                                    "text": "AI safety is a crucial field that focuses on ensuring AI systems behave as intended...",
                                    "source_url": "https://example.com/chapter1",
                                    "chapter": "Introduction to AI Safety",
                                    "position": 1,
                                    "relevance_score": 0.89
                                }
                            ]
                        },
                        "timestamp": "2023-12-11T10:30:00.123456Z",
                        "request_id": "677e2553-ddc3-49e2-8e40-28a3b4e53b7f"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "VECTOR_DB_QUERY_FAILED",
                            "message": "Failed to query vector database: [error details]"
                        }
                    }
                }
            }
        }
    }
)
async def query_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Query the vector database directly and return relevant chunks without AI processing.

    This endpoint bypasses the AI generation step and returns the raw, relevant text chunks
    from the vector database based on similarity search. It's useful for debugging or
    when you want to see the raw source material without AI interpretation.
    """
    start_time = time.time()

    # Sanitize inputs to prevent injection
    sanitized_question = html.escape(request.question) if request.question else ""
    sanitized_selected_text = html.escape(request.selected_text) if request.selected_text else None

    try:
        # Use retrieval service to get relevant chunks with sanitized inputs
        if request.context_mode == "selected_text" and sanitized_selected_text:
            results = retrieval_service.retrieve_chunks_by_selected_text(sanitized_selected_text)
        else:
            results = retrieval_service.retrieve_chunks(sanitized_question)

        response_time = (time.time() - start_time) * 1000
        monitoring_service.record_request("/v1/query", response_time, 200)

        return {
            "success": True,
            "data": {
                "query": sanitized_question,
                "results": results
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        monitoring_service.record_request("/v1/query", response_time, 500)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "VECTOR_DB_QUERY_FAILED",
                    "message": f"Failed to query vector database: {str(e)}"
                }
            }
        )