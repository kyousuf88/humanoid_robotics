from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from src.utils.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QdrantService:
    """
    Service for handling Qdrant vector database operations with error handling.
    """

    def __init__(self):
        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                timeout=10  # 10 seconds timeout
            )
            self.is_connected = True
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.client = None
            self.is_connected = False

        # Create collection if it doesn't exist
        if self.is_connected:
            self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the book_embeddings collection exists in Qdrant"""
        try:
            collections = self.client.get_collections()
            collection_exists = any(col.name == "book_embeddings" for col in collections.collections)

            if not collection_exists:
                self.client.create_collection(
                    collection_name="book_embeddings",
                    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),  # Cohere multilingual-v3 returns 1024-dim vectors
                )
                logger.info("Created 'book_embeddings' collection in Qdrant")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            self.is_connected = False

    def upsert_vectors(self, points: List[PointStruct]) -> bool:
        """
        Upsert vectors into the Qdrant collection.

        Args:
            points: List of PointStruct objects to upsert

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected:
            logger.error("Qdrant is not connected, cannot upsert vectors")
            return False

        try:
            self.client.upsert(
                collection_name="book_embeddings",
                points=points
            )
            return True
        except Exception as e:
            logger.error(f"Error upserting vectors to Qdrant: {e}")
            self.is_connected = False
            return False

    def search_vectors(self, vector: List[float], top_k: int = 5, score_threshold: float = 0.75) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant.

        Args:
            vector: Query vector to search for
            top_k: Number of results to return
            score_threshold: Minimum similarity score threshold

        Returns:
            List of search results
        """
        if not self.is_connected:
            logger.error("Qdrant is not connected, cannot search vectors")
            return []

        try:
            search_results = self.client.search(
                collection_name="book_embeddings",
                query_vector=vector,
                limit=top_k,
                score_threshold=score_threshold
            )

            results = []
            for hit in search_results:
                result = {
                    "id": hit.id,
                    "payload": hit.payload,
                    "score": hit.score
                }
                results.append(result)

            return results
        except Exception as e:
            logger.error(f"Error searching vectors in Qdrant: {e}")
            self.is_connected = False
            return []

    def retrieve_by_ids(self, ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve vectors by their IDs from Qdrant.

        Args:
            ids: List of IDs to retrieve

        Returns:
            List of retrieved vectors
        """
        if not self.is_connected:
            logger.error("Qdrant is not connected, cannot retrieve vectors by IDs")
            return []

        try:
            records = self.client.retrieve(
                collection_name="book_embeddings",
                ids=ids
            )

            results = []
            for record in records:
                result = {
                    "id": record.id,
                    "payload": record.payload
                }
                results.append(result)

            return results
        except Exception as e:
            logger.error(f"Error retrieving vectors by IDs from Qdrant: {e}")
            self.is_connected = False
            return []

    def check_connection(self) -> bool:
        """
        Check if the Qdrant connection is still active.

        Returns:
            True if connected, False otherwise
        """
        if not self.is_connected:
            return False

        try:
            # Try to get collections as a simple connection check
            self.client.get_collections()
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"Qdrant connection check failed: {e}")
            self.is_connected = False
            return False

    def get_collection_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the book_embeddings collection.

        Returns:
            Collection information or None if not connected
        """
        if not self.is_connected:
            logger.error("Qdrant is not connected, cannot get collection info")
            return None

        try:
            collection_info = self.client.get_collection("book_embeddings")
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "points_count": collection_info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info from Qdrant: {e}")
            self.is_connected = False
            return None