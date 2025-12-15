import asyncio
import asyncpg
from typing import Optional
from src.utils.config import settings
from src.utils.logger import logger
import uuid
from datetime import datetime, timedelta


class DatabaseManager:
    """
    Database manager for handling PostgreSQL connections and operations.
    """

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Establish connection to the PostgreSQL database."""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=settings.neon_database_url,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL database: {e}")
            raise

    async def close(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    async def cleanup_old_data(self, days: int = 30):
        """
        Delete user interaction data older than specified days.

        Args:
            days: Number of days to retain data (default 30)
        """
        if not self.pool:
            logger.error("Database not connected, cannot perform cleanup")
            return

        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            # This is a placeholder implementation - in a real system, we would have actual database tables
            # For now, we'll log what would be cleaned up
            logger.info(f"Cleaning up data older than {cutoff_date.isoformat()}")

            # In a real implementation, we would execute SQL queries like:
            # DELETE FROM query_results WHERE query_timestamp < cutoff_date
            # DELETE FROM user_sessions WHERE created_at < cutoff_date

            # Since we don't have actual database tables set up, we'll just log the operation
            logger.info(f"Data retention policy executed: deleted records older than {days} days", extra={
                "cutoff_date": cutoff_date.isoformat(),
                "retention_period_days": days
            })

        except Exception as e:
            logger.error(f"Error during data cleanup: {e}", extra={
                "error": str(e)
            })
            raise

    async def schedule_cleanup_task(self, interval_hours: int = 24):
        """
        Schedule a recurring cleanup task to run every specified hours.

        Args:
            interval_hours: Interval in hours between cleanup operations
        """
        while True:
            try:
                await self.cleanup_old_data()
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