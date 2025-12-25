from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
import uuid
from src.utils.cache_service import cache_service

router = APIRouter()


@router.get("/cache/stats", summary="Get Cache Statistics", description="Retrieve cache performance statistics.")
async def get_cache_stats() -> Dict[str, Any]:
    """
    Retrieve cache performance statistics.

    This endpoint provides information about the current state of the cache,
    including size, hit rate, and configuration.
    """
    stats = cache_service.get_stats()

    return {
        "success": True,
        "data": {
            "stats": stats,
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    }


@router.post("/cache/clear", summary="Clear Cache", description="Clear all cached data.")
async def clear_cache() -> Dict[str, Any]:
    """
    Clear all cached data.

    This endpoint clears the entire cache. Use with caution in production.
    """
    cache_service.clear_cache()

    return {
        "success": True,
        "message": "Cache cleared successfully",
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }


@router.post("/cache/question/invalidate", summary="Invalidate Question Cache", description="Remove cached response for a specific question.")
async def invalidate_question_cache(
    question: str,
    context_mode: str = "full_book",
    selected_text: str = None
) -> Dict[str, Any]:
    """
    Remove cached response for a specific question.

    This endpoint allows you to invalidate the cache for a specific question,
    forcing the next request for that question to be processed fresh.
    """
    cache_service.invalidate_question(question, context_mode, selected_text)

    return {
        "success": True,
        "message": "Question cache invalidated successfully",
        "question": question,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }