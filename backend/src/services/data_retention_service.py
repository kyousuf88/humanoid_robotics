import asyncio
from typing import Optional, List, Dict, Any
from src.utils.config import settings
from src.utils.logger import logger
import uuid
from datetime import datetime, timedelta
import json
import sqlite3
import threading
import time
import os


class DataRetentionService:
    """
    Service for handling data retention policy - automatically deleting
    user interaction data after 30 days.
    """

    def __init__(self):
        self.db_path = "rag_chatbot_test.db"
        self.lock = threading.Lock()

    def _get_connection(self):
        """Get a thread-safe database connection."""
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _create_tables(self):
        """Create necessary tables for storing user interaction data."""
        conn = self._get_connection()
        try:
            # Create query_results table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_results (
                    id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    source_citations TEXT NOT NULL,
                    relevance_score REAL NOT NULL,
                    query_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT
                )
            """)

            # Create user_sessions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id TEXT PRIMARY KEY,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_activity TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    selected_text TEXT,
                    rate_limit_remaining INTEGER NOT NULL DEFAULT 100,
                    rate_limit_reset TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes for efficient cleanup
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_query_results_timestamp
                ON query_results(query_timestamp)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_sessions_created_at
                ON user_sessions(created_at)
            """)

            conn.commit()
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            conn.close()

    async def initialize(self):
        """Initialize the database connection."""
        try:
            # Create necessary tables if they don't exist
            self._create_tables()
            logger.info("Data retention service initialized with SQLite database")
        except Exception as e:
            logger.error(f"Failed to initialize data retention service: {e}")
            raise

    async def cleanup_old_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Delete user interaction data older than specified days.

        Args:
            days: Number of days to retain data (default 30)

        Returns:
            Dictionary with cleanup statistics
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            cutoff_str = cutoff_date.isoformat()

            conn = self._get_connection()
            try:
                # Count records that will be deleted
                old_query_count = conn.execute(
                    "SELECT COUNT(*) FROM query_results WHERE query_timestamp < ?",
                    (cutoff_str,)
                ).fetchone()[0]

                old_session_count = conn.execute(
                    "SELECT COUNT(*) FROM user_sessions WHERE created_at < ?",
                    (cutoff_str,)
                ).fetchone()[0]

                # Delete old query results
                conn.execute(
                    "DELETE FROM query_results WHERE query_timestamp < ?",
                    (cutoff_str,)
                )
                deleted_query_count = conn.total_changes

                # Delete old user sessions
                conn.execute(
                    "DELETE FROM user_sessions WHERE created_at < ?",
                    (cutoff_str,)
                )
                deleted_session_count = conn.total_changes

                conn.commit()

                logger.info("Data retention cleanup completed", extra={
                    "cutoff_date": cutoff_str,
                    "retention_period_days": days,
                    "deleted_query_count": deleted_query_count,
                    "deleted_session_count": deleted_session_count
                })

                return {
                    "success": True,
                    "cutoff_date": cutoff_str,
                    "retention_period_days": days,
                    "deleted_query_count": deleted_query_count,
                    "deleted_session_count": deleted_session_count,
                    "message": f"Successfully deleted {deleted_query_count} query results and {deleted_session_count} user sessions older than {days} days"
                }

            except Exception as e:
                logger.error(f"Error during data cleanup: {e}", extra={
                    "error": str(e)
                })
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to clean up old data: {str(e)}"
                }
            finally:
                conn.close()

        except Exception as e:
            logger.error(f"Error during data cleanup: {e}", extra={
                "error": str(e)
            })
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to clean up old data: {str(e)}"
            }

    async def schedule_cleanup_task(self, interval_hours: int = 24) -> asyncio.Task:
        """
        Schedule a recurring cleanup task to run every specified hours.

        Args:
            interval_hours: Interval in hours between cleanup operations

        Returns:
            asyncio.Task object for the scheduled cleanup task
        """
        async def cleanup_loop():
            while True:
                try:
                    result = await self.cleanup_old_data()
                    if result["success"]:
                        logger.info(f"Scheduled data cleanup completed: {result['message']}")
                    else:
                        logger.error(f"Scheduled data cleanup failed: {result['message']}")

                    # Wait for the specified interval before running again
                    await asyncio.sleep(interval_hours * 3600)
                except asyncio.CancelledError:
                    logger.info("Data cleanup task was cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in scheduled cleanup task: {e}", extra={
                        "error": str(e)
                    })
                    # Wait before retrying to avoid rapid error loops
                    await asyncio.sleep(300)  # Wait 5 minutes before retrying

        # Create and return the task
        task = asyncio.create_task(cleanup_loop())
        logger.info(f"Scheduled data retention cleanup task to run every {interval_hours} hours")
        return task

    async def get_retention_stats(self) -> Dict[str, Any]:
        """
        Get statistics about data retention including how much data would be affected
        by the retention policy.

        Returns:
            Dictionary with retention statistics
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            cutoff_str = cutoff_date.isoformat()

            conn = self._get_connection()
            try:
                # Count old records that would be deleted
                old_query_count = conn.execute(
                    "SELECT COUNT(*) FROM query_results WHERE query_timestamp < ?",
                    (cutoff_str,)
                ).fetchone()[0]

                old_session_count = conn.execute(
                    "SELECT COUNT(*) FROM user_sessions WHERE created_at < ?",
                    (cutoff_str,)
                ).fetchone()[0]

                # Count total records
                total_query_count = conn.execute(
                    "SELECT COUNT(*) FROM query_results"
                ).fetchone()[0]

                total_session_count = conn.execute(
                    "SELECT COUNT(*) FROM user_sessions"
                ).fetchone()[0]

                return {
                    "success": True,
                    "retention_policy_days": 30,
                    "cutoff_date": cutoff_str,
                    "would_delete": {
                        "query_results": old_query_count,
                        "user_sessions": old_session_count
                    },
                    "total_records": {
                        "query_results": total_query_count,
                        "user_sessions": total_session_count
                    },
                    "message": f"Found {old_query_count} query results and {old_session_count} user sessions that would be deleted under current retention policy"
                }

            except Exception as e:
                logger.error(f"Error getting retention stats: {e}", extra={
                    "error": str(e)
                })
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to get retention stats: {str(e)}"
                }
            finally:
                conn.close()

        except Exception as e:
            logger.error(f"Error getting retention stats: {e}", extra={
                "error": str(e)
            })
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get retention stats: {str(e)}"
            }

    async def close(self):
        """Close the database connection."""
        logger.info("Data retention service database connection closed")