from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from src.utils.logger import logger
import re


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security middleware to add security headers and perform basic security checks.
    """

    async def dispatch(self, request: Request, call_next):
        # Add security headers to the response
        response: StarletteResponse = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"  # or "SAMEORIGIN" if needed
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self';"

        # Additional security checks during request processing
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not self._is_valid_content_type(content_type):
                logger.warning("Invalid content type detected", extra={
                    "content_type": content_type,
                    "path": str(request.url.path),
                    "method": request.method
                })
                return StarletteResponse(
                    status_code=400,
                    content="Invalid content type"
                )

        return response

    def _is_valid_content_type(self, content_type: str) -> bool:
        """
        Check if the content type is valid and safe.
        """
        valid_content_types = [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain"
        ]

        # Clean and normalize the content type
        clean_content_type = content_type.split(";")[0].strip().lower()

        return clean_content_type in valid_content_types


def security_headers_middleware(app):
    """
    Add security headers to all responses.
    """
    async def middleware(request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"

        return response

    return middleware