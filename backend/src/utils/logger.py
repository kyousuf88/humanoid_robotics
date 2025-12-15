import logging
from datetime import datetime
from typing import Dict, Any
import json
import os


class CustomFormatter(logging.Formatter):
    """Custom formatter to add color and structure to logs"""

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    """Centralized logging utility for the application"""

    def __init__(self, name: str = "rag_chatbot", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding multiple handlers if logger already exists
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            # Create file handler
            file_handler = logging.FileHandler("app.log")
            file_handler.setLevel(level)

            # Create formatters and add them to handlers
            console_formatter = CustomFormatter()
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )

            console_handler.setFormatter(console_formatter)
            file_handler.setFormatter(file_formatter)

            # Add handlers to the logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log an info message"""
        self._log(logging.INFO, message, extra)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log a warning message"""
        self._log(logging.WARNING, message, extra)

    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log an error message"""
        self._log(logging.ERROR, message, extra)

    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log a debug message"""
        self._log(logging.DEBUG, message, extra)

    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log a critical message"""
        self._log(logging.CRITICAL, message, extra)

    def _log(self, level: int, message: str, extra: Dict[str, Any] = None):
        """Internal method to log messages"""
        if extra:
            # Add extra information to the log
            extra_str = json.dumps(extra, default=str)
            message = f"{message} | Extra: {extra_str}"

        self.logger.log(level, message)

    def log_interaction(self, session_id: str, question: str, answer: str,
                       relevance_score: float = None, source_citations: list = None):
        """Log a user interaction with the chatbot"""
        interaction_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "question": question,
            "answer_length": len(answer) if answer else 0,
            "relevance_score": relevance_score,
            "citation_count": len(source_citations) if source_citations else 0
        }

        self.info("User interaction", extra=interaction_data)

    def log_performance(self, endpoint: str, response_time_ms: float,
                       status_code: int = 200, user_id: str = None):
        """Log performance metrics for API endpoints"""
        performance_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "response_time_ms": response_time_ms,
            "status_code": status_code,
            "user_id": user_id
        }

        # Log slow responses as warnings
        if response_time_ms > 800:  # Threshold for slow responses
            self.warning("Slow API response", extra=performance_data)
        else:
            self.info("API request", extra=performance_data)

    def log_error(self, error: Exception, context: str = "", extra: Dict[str, Any] = None):
        """Log an error with context"""
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "extra": extra
        }

        self.error("Application error", extra=error_data)


# Global logger instance
def get_logger(name: str = "rag_chatbot") -> Logger:
    """Get a logger instance"""
    return Logger(name=name)


# Create the default logger
logger = get_logger()