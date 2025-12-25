from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from src.services.embedding_service import EmbeddingService
from src.services.qdrant_service import QdrantService
from src.models.book_chunk import BookChunk
from src.utils.data_validator import DataValidator
from datetime import datetime
import time
import uuid
from src.utils.monitoring_service import monitoring_service

router = APIRouter()
embedding_service = EmbeddingService()
qdrant_service = QdrantService()


class TextChunk(BaseModel):
    """Model for a text chunk to be embedded"""
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text content to embed",
        example="The concept of artificial intelligence has evolved significantly over the past decades."
    )
    source_url: str = Field(
        ...,
        max_length=2048,
        description="URL of the source page in the Docusaurus book",
        example="https://example.com/chapter1"
    )
    chapter: str = Field(
        ...,
        max_length=255,
        description="Chapter or section name where this chunk appears",
        example="Chapter 1: Introduction"
    )
    position: int = Field(
        ...,
        ge=1,
        description="Sequential position of this chunk within the chapter",
        example=1
    )


class EmbedRequest(BaseModel):
    """Request model for the embed endpoint"""
    text_chunks: List[TextChunk] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of text chunks to generate embeddings for",
        example=[
            {
                "text": "The concept of artificial intelligence has evolved significantly over the past decades.",
                "source_url": "https://example.com/chapter1",
                "chapter": "Chapter 1: Introduction",
                "position": 1
            }
        ]
    )


class EmbedResponse(BaseModel):
    """Response model for the embed endpoint"""
    success: bool = Field(..., description="Indicates if the request was successful")
    data: Dict[str, Any] = Field(..., description="The response data containing processing results")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the response")
    request_id: str = Field(..., description="Unique identifier for the request")


@router.post(
    "/embed",
    summary="Generate Embeddings",
    description="Generate embeddings for text content and store in vector database.",
    responses={
        200: {
            "description": "Successful response with embedding processing results",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "processed_count": 1,
                            "stored_chunk_ids": ["550e8400-e29b-41d4-a716-446655440000"],
                            "status": "completed"
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
                            "message": "One or more text chunks are invalid"
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
                            "code": "EMBEDDING_GENERATION_FAILED",
                            "message": "Failed to generate embeddings: [error details]"
                        }
                    }
                }
            }
        }
    }
)
async def embed_endpoint(request: EmbedRequest) -> Dict[str, Any]:
    """
    Generate embeddings for text content and store in vector database.

    This endpoint takes text chunks, generates embeddings using Cohere, and stores
    them in Qdrant vector database with appropriate metadata for later retrieval.
    """
    start_time = time.time()

    try:
        # Validate all text chunks
        valid_chunks = []
        for chunk_data in request.text_chunks:
            # Create a temporary BookChunk for validation
            temp_chunk = BookChunk(
                text_content=chunk_data.text,
                source_url=chunk_data.source_url,
                chapter=chunk_data.chapter,
                position=chunk_data.position
            )

            if DataValidator.validate_book_chunk(temp_chunk):
                valid_chunks.append(chunk_data)
            else:
                monitoring_service.record_request("/v1/embed", (time.time() - start_time) * 1000, 400)
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": {
                            "code": "INVALID_INPUT",
                            "message": f"Invalid text chunk at position {chunk_data.position} in chapter '{chunk_data.chapter}'"
                        }
                    }
                )

        # Generate embeddings for valid chunks
        embedding_results = await embedding_service.embed_chunks([
            {
                "text": chunk.text,
                "source_url": chunk.source_url,
                "chapter": chunk.chapter,
                "position": chunk.position
            }
            for chunk in valid_chunks
        ])

        # Store embeddings in Qdrant
        stored_chunk_ids = []
        for result in embedding_results:
            if result.get("success"):
                stored_chunk_ids.append(result.get("chunk_id"))

        # Store in Qdrant database
        success = qdrant_service.upsert_vectors(embedding_results)

        if not success:
            monitoring_service.record_request("/v1/embed", (time.time() - start_time) * 1000, 500)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": {
                        "code": "VECTOR_DB_STORE_FAILED",
                        "message": "Failed to store embeddings in vector database"
                    }
                }
            )

        response_time = (time.time() - start_time) * 1000
        monitoring_service.record_request("/v1/embed", response_time, 200)

        return {
            "success": True,
            "data": {
                "processed_count": len(valid_chunks),
                "stored_chunk_ids": stored_chunk_ids,
                "status": "completed"
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        monitoring_service.record_request("/v1/embed", response_time, 500)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "EMBEDDING_GENERATION_FAILED",
                    "message": f"Failed to generate embeddings: {str(e)}"
                }
            }
        )