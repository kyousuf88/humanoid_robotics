from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
import uuid
from src.utils.monitoring_service import monitoring_service

router = APIRouter()


@router.get("/metrics", summary="Get Application Metrics", description="Retrieve current application metrics and performance statistics.")
async def get_metrics() -> Dict[str, Any]:
    """
    Retrieve current application metrics and performance statistics.

    This endpoint provides real-time metrics about the application's performance,
    including request rates, error rates, response times, and endpoint-specific statistics.
    """
    metrics = monitoring_service.get_current_metrics()

    return {
        "success": True,
        "data": {
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    }


@router.get("/alerts", summary="Get Current Alerts", description="Retrieve any active monitoring alerts.")
async def get_alerts() -> Dict[str, Any]:
    """
    Retrieve any active monitoring alerts.

    This endpoint checks if any metrics have crossed their configured thresholds
    and returns information about any active alerts.
    """
    alerts = monitoring_service.get_alerts()

    return {
        "success": True,
        "data": alerts,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }