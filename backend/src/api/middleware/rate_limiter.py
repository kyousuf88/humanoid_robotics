import time
from typing import Dict
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from collections import defaultdict


class RateLimiter:
    """
    Token bucket algorithm for rate limiting requests per session/IP.
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.buckets: Dict[str, dict] = defaultdict(self._create_bucket)

    def _create_bucket(self) -> dict:
        """Create a new rate limiting bucket with initial values"""
        return {
            "tokens": self.max_requests,
            "last_refill": time.time()
        }

    def _refill_tokens(self, bucket: dict) -> None:
        """Refill tokens based on time passed since last refill"""
        now = time.time()
        time_passed = now - bucket["last_refill"]

        # Calculate how many tokens to add based on time passed
        tokens_to_add = time_passed * (self.max_requests / self.window_seconds)
        bucket["tokens"] = min(self.max_requests, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = now

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.

        Args:
            identifier: A unique identifier for the user (session ID, IP, etc.)

        Returns:
            True if request is allowed, False otherwise
        """
        bucket = self.buckets[identifier]
        self._refill_tokens(bucket)

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        return False

    def get_remaining_requests(self, identifier: str) -> int:
        """Get the number of remaining requests for the identifier"""
        bucket = self.buckets[identifier]
        self._refill_tokens(bucket)
        return int(bucket["tokens"])

    def get_reset_time(self, identifier: str) -> datetime:
        """Get the time when the rate limit will reset for the identifier"""
        return datetime.utcnow() + timedelta(seconds=self.window_seconds)


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)  # 100 requests per hour


async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting requests.
    """
    # Extract client IP or session token for rate limiting
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    session_token = request.headers.get("session-token", client_ip)

    # Check if request is allowed
    if not rate_limiter.is_allowed(session_token):
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Rate limit exceeded. Please try again later."
                }
            }
        )

    # Add rate limit headers to response
    response = await call_next(request)

    remaining = rate_limiter.get_remaining_requests(session_token)
    reset_time = rate_limiter.get_reset_time(session_token)

    response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = reset_time.isoformat()

    return response