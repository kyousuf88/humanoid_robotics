import asyncio
import asyncpg
from typing import Optional, List, Dict, Any
from src.utils.config import settings
from src.utils.logger import logger
import uuid
from datetime import datetime, timedelta
import json


class DataRetentionService:
    """
    Service for handling data retention policy - automatically deleting
    user interaction data after 30 days.
    """

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def initialize(self):
        """Initialize the database connection."""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=settings.neon_database_url,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
            logger.info("Data retention service initialized with database connection")

            # Create necessary tables if they don't exist
            await self._create_tables()
        except Exception as e:
            logger.error(f"Failed to initialize data retention service: {e}")
            raise

    async def _create_tables(self):
        """Create necessary tables for storing user interaction data."""
        if not self.pool:
            return

        async with self.pool.acquire() as conn:
            # Create query_results table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS query_results (
                    id UUID PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    source_citations JSONB NOT NULL,
                    relevance_score FLOAT NOT NULL,
                    retrieved_chunks UUID[],
                    query_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    session_id UUID
                )
            """)

            # Create user_sessions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id UUID PRIMARY KEY,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    last_activity TIMESTAMP NOT NULL DEFAULT NOW(),
                    selected_text TEXT,
                    query_history UUID[],
                    rate_limit_remaining INTEGER NOT NULL DEFAULT 100,
                    rate_limit_reset TIMESTAMP NOT NULL DEFAULT NOW(),
                    context_preservation JSONB
                )
            """)

            # Create indexes for efficient cleanup
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_query_results_timestamp
                ON query_results(query_timestamp)
            """)

            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_sessions_created_at
                ON user_sessions(created_at)
            """)

    async def cleanup_old_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Delete user interaction data older than specified days.

        Args:
            days: Number of days to retain data (default 30)

        Returns:
            Dictionary with cleanup statistics
        """
        if not self.pool:
            logger.error("Database not connected, cannot perform cleanup")
            return {"success": False, "message": "Database not connected"}

        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            async with self.pool.acquire() as conn:
                # Count records that will be deleted
                old_query_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM query_results WHERE query_timestamp < $1",
                    cutoff_date
                )

                old_session_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM user_sessions WHERE created_at < $1",
                    cutoff_date
                )

                # Delete old query results
                deleted_queries = await conn.execute(
                    "DELETE FROM query_results WHERE query_timestamp < $1",
                    cutoff_date
                )

                # Delete old user sessions
                deleted_sessions = await conn.execute(
                    "DELETE FROM user_sessions WHERE created_at < $1",
                    cutoff_date
                )

                # Get actual deleted counts
                deleted_query_count = int(deleted_queries.split()[1]) if 'DELETE' in deleted_queries else old_query_count
                deleted_session_count = int(deleted_sessions.split()[1]) if 'DELETE' in deleted_sessions else old_session_count

                logger.info("Data retention cleanup completed", extra={
                    "cutoff_date": cutoff_date.isoformat(),
                    "retention_period_days": days,
                    "deleted_query_count": deleted_query_count,
                    "deleted_session_count": deleted_session_count
                })

                return {
                    "success": True,
                    "cutoff_date": cutoff_date.isoformat(),
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
        if not self.pool:
            return {"success": False, "message": "Database not connected"}

        try:
            cutoff_date = datetime.utcnow() - timedelta(days=30)

            async with self.pool.acquire() as conn:
                # Count old records that would be deleted
                old_query_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM query_results WHERE query_timestamp < $1",
                    cutoff_date
                )

                old_session_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM user_sessions WHERE created_at < $1",
                    cutoff_date
                )

                # Count total records
                total_query_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM query_results"
                )

                total_session_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM user_sessions"
                )

                return {
                    "success": True,
                    "retention_policy_days": 30,
                    "cutoff_date": cutoff_date.isoformat(),
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

    async def close(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Data retention service database connection pool closed")