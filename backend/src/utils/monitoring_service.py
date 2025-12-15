from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import time
import asyncio
from src.utils.logger import logger
from src.utils.config import settings


class MetricsCollector:
    """
    Collects and stores application metrics for monitoring and alerting.
    """

    def __init__(self):
        # Store metrics in memory (in production, use Redis or a time-series database)
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self.endpoint_counts = defaultdict(int)
        self.endpoint_errors = defaultdict(int)
        self.rate_limit_counts = defaultdict(int)

        # Track metrics over time windows
        self.metrics_by_window = defaultdict(lambda: {
            'requests': 0,
            'errors': 0,
            'total_response_time': 0.0,
            'avg_response_time': 0.0
        })

    def record_request(self, endpoint: str, response_time_ms: float, status_code: int = 200):
        """Record a request and its response time."""
        self.request_count += 1
        self.response_times.append(response_time_ms)
        self.endpoint_counts[endpoint] += 1

        # Update current time window metrics
        current_window = self._get_current_window()
        self.metrics_by_window[current_window]['requests'] += 1
        self.metrics_by_window[current_window]['total_response_time'] += response_time_ms

        if status_code >= 400:
            self.error_count += 1
            self.endpoint_errors[endpoint] += 1
            self.metrics_by_window[current_window]['errors'] += 1

    def record_rate_limit(self, endpoint: str):
        """Record a rate limit event."""
        self.rate_limit_counts[endpoint] += 1

    def _get_current_window(self) -> str:
        """Get the current 5-minute window as a string."""
        now = datetime.utcnow()
        # Round down to nearest 5 minutes
        rounded_time = now - timedelta(minutes=now.minute % 5, seconds=now.second, microseconds=now.microsecond)
        return rounded_time.isoformat()

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics summary."""
        if len(self.response_times) > 0:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            p95_response_time = sorted(self.response_times)[int(0.95 * len(self.response_times))] if self.response_times else 0
            max_response_time = max(self.response_times) if self.response_times else 0
        else:
            avg_response_time = 0
            p95_response_time = 0
            max_response_time = 0

        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0

        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate_percentage": round(error_rate, 2),
            "avg_response_time_ms": round(avg_response_time, 2),
            "p95_response_time_ms": p95_response_time,
            "max_response_time_ms": max_response_time,
            "requests_per_minute": self._get_requests_per_minute(),
            "endpoint_stats": {
                endpoint: {
                    "requests": count,
                    "errors": self.endpoint_errors[endpoint],
                    "error_rate": round(self.endpoint_errors[endpoint] / count * 100, 2) if count > 0 else 0
                }
                for endpoint, count in self.endpoint_counts.items()
            },
            "rate_limit_events": dict(self.rate_limit_counts)
        }

    def _get_requests_per_minute(self) -> float:
        """Calculate approximate requests per minute based on recent activity."""
        if not self.response_times:
            return 0

        # Use the last 60 seconds of data if available
        recent_requests = [rt for rt in self.response_times if rt is not None]
        if len(recent_requests) == 0:
            return 0

        # This is a simplified calculation - in a real system you'd track requests over time windows
        return len(recent_requests)  # Placeholder - would need more sophisticated tracking

    def check_alerts(self) -> Dict[str, Any]:
        """Check if any metrics have crossed alert thresholds."""
        alerts = []
        current_metrics = self.get_current_metrics()

        # Check error rate threshold
        if current_metrics["error_rate_percentage"] > 5:  # 5% error rate threshold
            alerts.append({
                "alert": "HIGH_ERROR_RATE",
                "message": f"Error rate is {current_metrics['error_rate_percentage']}% which exceeds 5% threshold",
                "severity": "HIGH",
                "value": current_metrics["error_rate_percentage"],
                "threshold": 5
            })

        # Check response time threshold
        if current_metrics["p95_response_time_ms"] > 800:  # 800ms response time threshold
            alerts.append({
                "alert": "HIGH_RESPONSE_TIME",
                "message": f"P95 response time is {current_metrics['p95_response_time_ms']}ms which exceeds 800ms threshold",
                "severity": "MEDIUM",
                "value": current_metrics["p95_response_time_ms"],
                "threshold": 800
            })

        # Check requests per minute threshold (for potential DDoS)
        if current_metrics["requests_per_minute"] > 1000:  # 1000 requests/minute threshold
            alerts.append({
                "alert": "HIGH_TRAFFIC",
                "message": f"Requests per minute is {current_metrics['requests_per_minute']} which exceeds 1000 threshold",
                "severity": "MEDIUM",
                "value": current_metrics["requests_per_minute"],
                "threshold": 1000
            })

        return {
            "alerts": alerts,
            "has_alerts": len(alerts) > 0,
            "timestamp": datetime.utcnow().isoformat()
        }


class MonitoringService:
    """
    Main monitoring service that collects metrics and handles alerting.
    """

    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_callbacks = []
        self.is_monitoring = False
        self.monitoring_task: Optional[asyncio.Task] = None

    def add_alert_callback(self, callback):
        """Add a callback function to be called when alerts are triggered."""
        self.alert_callbacks.append(callback)

    def record_request(self, endpoint: str, response_time_ms: float, status_code: int = 200):
        """Record a request with its metrics."""
        self.metrics_collector.record_request(endpoint, response_time_ms, status_code)

        # Check for alerts and trigger callbacks if needed
        alerts_result = self.metrics_collector.check_alerts()
        if alerts_result["has_alerts"]:
            self._trigger_alerts(alerts_result)

    def record_rate_limit(self, endpoint: str):
        """Record a rate limit event."""
        self.metrics_collector.record_rate_limit(endpoint)

    def _trigger_alerts(self, alerts_result: Dict[str, Any]):
        """Trigger alert callbacks."""
        for callback in self.alert_callbacks:
            try:
                callback(alerts_result)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}", extra={
                    "callback": str(callback),
                    "error": str(e)
                })

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics summary."""
        return self.metrics_collector.get_current_metrics()

    def get_alerts(self) -> Dict[str, Any]:
        """Get current alerts."""
        return self.metrics_collector.check_alerts()

    async def start_monitoring(self):
        """Start periodic monitoring task."""
        if self.is_monitoring:
            return

        self.is_monitoring = True

        async def monitoring_loop():
            while self.is_monitoring:
                try:
                    # Log metrics every 5 minutes
                    current_metrics = self.get_current_metrics()
                    logger.info("Periodic metrics report", extra=current_metrics)

                    # Check for alerts
                    alerts_result = self.get_alerts()
                    if alerts_result["has_alerts"]:
                        logger.warning("Monitoring alerts triggered", extra=alerts_result)

                    # Sleep for 5 minutes
                    await asyncio.sleep(300)
                except asyncio.CancelledError:
                    logger.info("Monitoring task cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}", extra={
                        "error": str(e)
                    })
                    await asyncio.sleep(60)  # Wait 1 minute before retrying

        self.monitoring_task = asyncio.create_task(monitoring_loop())
        logger.info("Started monitoring service")

    async def stop_monitoring(self):
        """Stop the monitoring task."""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped monitoring service")


# Global monitoring service instance
monitoring_service = MonitoringService()


def monitor_endpoint(endpoint_name: str):
    """
    Decorator to monitor endpoint performance.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                monitoring_service.record_request(endpoint_name, response_time, 200)
                return result
            except Exception as e:
                response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                # Determine status code based on exception type
                if hasattr(e, 'status_code'):
                    status_code = e.status_code
                else:
                    status_code = 500
                monitoring_service.record_request(endpoint_name, response_time, status_code)
                raise
        return wrapper
    return decorator