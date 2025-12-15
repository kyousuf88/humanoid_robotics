from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

# Import routers
from .routes.health import router as health_router
from .routes.session import router as session_router
from .routes.monitoring import router as monitoring_router
from .routes.cache import router as cache_router
from .middleware.rate_limiter import rate_limit_middleware
from .middleware.security import SecurityMiddleware
from src.services.data_retention_service import DataRetentionService
from src.utils.monitoring_service import monitoring_service

# Global instances of services
data_retention_service: DataRetentionService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown events."""
    global data_retention_service

    # Startup
    data_retention_service = DataRetentionService()
    try:
        await data_retention_service.initialize()
        # Start the scheduled cleanup task
        cleanup_task = await data_retention_service.schedule_cleanup_task()

        # Start monitoring
        await monitoring_service.start_monitoring()
        yield
    finally:
        # Shutdown
        if data_retention_service:
            await data_retention_service.close()

        # Stop monitoring
        await monitoring_service.stop_monitoring()

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG (Retrieval-Augmented Generation) Chatbot for AI/Spec-Driven Book",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security middleware first (applies to all requests)
app.add_middleware(SecurityMiddleware)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Include routers
app.include_router(health_router, prefix="/v1", tags=["health"])
app.include_router(session_router, prefix="/v1", tags=["session"])
app.include_router(monitoring_router, prefix="/v1", tags=["monitoring"])
app.include_router(cache_router, prefix="/v1", tags=["cache"])

# Add a general exception handler for consistent error responses
@app.exception_handler(429)
async def rate_limit_handler(request, exc):
    return {
        "success": False,
        "error": {
            "code": "RATE_LIMIT_EXCEEDED",
            "message": "Rate limit exceeded. Please try again later."
        },
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }

@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {
        "message": "RAG Chatbot API is running",
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }

# For testing purposes, we'll also add a basic error endpoint
@app.get("/error-test")
async def test_error():
    """Test endpoint to simulate an error"""
    raise Exception("This is a test error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)