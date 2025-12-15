from typing import List, Dict, Any, Optional
from src.models.book_chunk import BookChunk
from src.utils.logger import logger


class DataValidator:
    """
    Utility class for validating book content ingestion data.
    """

    @staticmethod
    def validate_book_chunk(chunk: BookChunk) -> bool:
        """
        Validate a book chunk before ingestion.

        Args:
            chunk: The BookChunk object to validate

        Returns:
            True if valid, False otherwise
        """
        # Check if text_content is not empty or just whitespace
        if not chunk.text_content or not chunk.text_content.strip():
            logger.error("Book chunk has empty or whitespace-only text content", extra={
                "chunk_id": str(chunk.id),
                "source_url": chunk.source_url
            })
            return False

        # Check if text_content is too long (prevent extremely large chunks)
        if len(chunk.text_content) > 10000:  # 10k characters max
            logger.error("Book chunk text content exceeds maximum length", extra={
                "chunk_id": str(chunk.id),
                "source_url": chunk.source_url,
                "text_length": len(chunk.text_content)
            })
            return False

        # Check if source_url is valid
        if not chunk.source_url or not DataValidator._is_valid_url(chunk.source_url):
            logger.error("Book chunk has invalid source URL", extra={
                "chunk_id": str(chunk.id),
                "source_url": chunk.source_url
            })
            return False

        # Check if chapter is valid
        if not chunk.chapter or not chunk.chapter.strip():
            logger.warning("Book chunk has empty or invalid chapter", extra={
                "chunk_id": str(chunk.id),
                "source_url": chunk.source_url
            })
            # We'll allow empty chapters but log as warning

        # All checks passed
        return True

    @staticmethod
    def validate_book_chunks(chunks: List[BookChunk]) -> List[BookChunk]:
        """
        Validate a list of book chunks, returning only the valid ones.

        Args:
            chunks: List of BookChunk objects to validate

        Returns:
            List of valid BookChunk objects
        """
        valid_chunks = []
        invalid_count = 0

        for chunk in chunks:
            if DataValidator.validate_book_chunk(chunk):
                valid_chunks.append(chunk)
            else:
                invalid_count += 1

        logger.info("Book chunks validation completed", extra={
            "total_chunks": len(chunks),
            "valid_chunks": len(valid_chunks),
            "invalid_chunks": invalid_count
        })

        return valid_chunks

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """
        Basic URL validation.

        Args:
            url: URL string to validate

        Returns:
            True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False

        # Basic check for URL format
        url = url.strip().lower()
        return url.startswith(('http://', 'https://')) and len(url) > 10

    @staticmethod
    def validate_ingestion_data(data: Dict[str, Any]) -> bool:
        """
        Validate raw ingestion data before creating BookChunk objects.

        Args:
            data: Raw data dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ['text_content', 'source_url']

        for field in required_fields:
            if field not in data or data[field] is None:
                logger.error("Missing required field in ingestion data", extra={
                    "missing_field": field,
                    "available_fields": list(data.keys())
                })
                return False

        # Validate text_content
        text_content = data['text_content']
        if not isinstance(text_content, str) or not text_content.strip():
            logger.error("Invalid text content in ingestion data", extra={
                "text_content_type": type(text_content).__name__,
                "text_content_length": len(text_content) if isinstance(text_content, str) else 0
            })
            return False

        # Validate source_url
        source_url = data['source_url']
        if not isinstance(source_url, str) or not DataValidator._is_valid_url(source_url):
            logger.error("Invalid source URL in ingestion data", extra={
                "source_url": source_url,
                "source_url_type": type(source_url).__name__
            })
            return False

        # Optional field validations
        if 'chapter' in data and data['chapter'] is not None:
            if not isinstance(data['chapter'], str) or not data['chapter'].strip():
                logger.warning("Invalid chapter in ingestion data", extra={
                    "chapter_value": data['chapter'],
                    "chapter_type": type(data['chapter']).__name__
                })

        return True

    @staticmethod
    def validate_ingestion_batch(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate a batch of raw ingestion data.

        Args:
            data_list: List of raw data dictionaries to validate

        Returns:
            List of valid data dictionaries
        """
        valid_data = []
        invalid_count = 0

        for i, data in enumerate(data_list):
            if DataValidator.validate_ingestion_data(data):
                valid_data.append(data)
            else:
                invalid_count += 1
                logger.error(f"Invalid data at index {i}", extra={
                    "index": i,
                    "data_keys": list(data.keys())
                })

        logger.info("Ingestion data batch validation completed", extra={
            "total_items": len(data_list),
            "valid_items": len(valid_data),
            "invalid_items": invalid_count
        })

        return valid_data