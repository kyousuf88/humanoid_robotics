import time
from typing import Callable, Any
from functools import wraps
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def monitor_performance(timeout_ms: int = 800) -> Callable:
    """
    Decorator to monitor the performance of functions and ensure they meet response time targets.

    Args:
        timeout_ms: Maximum allowed execution time in milliseconds

    Returns:
        Decorated function with performance monitoring
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time_ms = (time.time() - start_time) * 1000

                # Log performance metrics
                logger.info(f"{func.__name__} executed in {execution_time_ms:.2f}ms")

                # Check if execution time exceeds the threshold
                if execution_time_ms > timeout_ms:
                    logger.warning(
                        f"{func.__name__} exceeded performance target of {timeout_ms}ms, "
                        f"took {execution_time_ms:.2f}ms"
                    )

                return result
            except Exception as e:
                execution_time_ms = (time.time() - start_time) * 1000
                logger.error(
                    f"{func.__name__} failed after {execution_time_ms:.2f}ms with error: {str(e)}"
                )
                raise

        return wrapper
    return decorator


class PerformanceMonitor:
    """
    Class to monitor and track performance metrics for the application.
    """
    def __init__(self, response_time_threshold: float = 800.0):  # 800ms threshold
        self.response_time_threshold = response_time_threshold  # in milliseconds
        self.metrics = {
            "total_requests": 0,
            "slow_requests": 0,  # Requests exceeding threshold
            "total_response_time": 0.0,  # in milliseconds
            "peak_response_time": 0.0,  # in milliseconds
            "start_time": datetime.utcnow()
        }

    def record_request(self, response_time_ms: float) -> None:
        """
        Record a request's response time.

        Args:
            response_time_ms: Response time in milliseconds
        """
        self.metrics["total_requests"] += 1
        self.metrics["total_response_time"] += response_time_ms

        if response_time_ms > self.response_time_threshold:
            self.metrics["slow_requests"] += 1

        if response_time_ms > self.metrics["peak_response_time"]:
            self.metrics["peak_response_time"] = response_time_ms

    def get_performance_stats(self) -> dict:
        """
        Get current performance statistics.

        Returns:
            Dictionary with performance metrics
        """
        if self.metrics["total_requests"] == 0:
            avg_response_time = 0.0
        else:
            avg_response_time = self.metrics["total_response_time"] / self.metrics["total_requests"]

        slow_request_percentage = 0.0
        if self.metrics["total_requests"] > 0:
            slow_request_percentage = (self.metrics["slow_requests"] / self.metrics["total_requests"]) * 100

        return {
            "total_requests": self.metrics["total_requests"],
            "slow_requests": self.metrics["slow_requests"],
            "slow_request_percentage": slow_request_percentage,
            "average_response_time_ms": avg_response_time,
            "peak_response_time_ms": self.metrics["peak_response_time"],
            "response_time_threshold_ms": self.response_time_threshold,
            "within_threshold_percentage": 100 - slow_request_percentage,
            "uptime_seconds": (datetime.utcnow() - self.metrics["start_time"]).total_seconds()
        }

    def is_within_performance_targets(self) -> bool:
        """
        Check if the service is meeting performance targets.

        Returns:
            True if 95% of requests are within the threshold, False otherwise
        """
        if self.metrics["total_requests"] == 0:
            return True  # No requests yet, so technically meeting targets

        success_rate = 1 - (self.metrics["slow_requests"] / self.metrics["total_requests"])
        return success_rate >= 0.95  # 95% of requests should be within threshold


# Global performance monitor instance
performance_monitor = PerformanceMonitor(response_time_threshold=800.0)


def track_response_time(func: Callable) -> Callable:
    """
    Decorator to track response time and update the global performance monitor.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            response_time_ms = (time.time() - start_time) * 1000
            performance_monitor.record_request(response_time_ms)
            return result
        except Exception:
            response_time_ms = (time.time() - start_time) * 1000
            performance_monitor.record_request(response_time_ms)  # Still record failed requests
            raise

    return wrapper