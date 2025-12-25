from typing import List, Dict, Any
from src.models.book_chunk import BookChunk
from src.services.retrieval_service import RetrievalService
from src.utils.config import settings
from src.utils.data_validator import DataValidator
import cohere
from urllib.parse import urlparse


class EmbeddingService:
    """
    Service for generating embeddings for text content and storing in vector database.
    """

    def __init__(self):
        self.cohere_client = cohere.Client(settings.cohere_api_key)
        self.retrieval_service = RetrievalService()

    def embed_text_chunks(self, text_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate embeddings for multiple text chunks and store them.

        Args:
            text_chunks: List of dictionaries containing text, source_url, chapter, and position

        Returns:
            Dictionary with processing results
        """
        # Validate the ingestion data first
        valid_chunks_data = DataValidator.validate_ingestion_batch(text_chunks)

        stored_chunk_ids = []
        processed_count = 0
        skipped_count = len(text_chunks) - len(valid_chunks_data)

        for chunk_data in valid_chunks_data:
            # Create a BookChunk object from the data
            book_chunk = BookChunk(
                text_content=chunk_data["text"],
                source_url=chunk_data["source_url"],
                chapter=chunk_data["chapter"],
                position=chunk_data["position"],
                metadata=chunk_data.get("metadata", {})
            )

            # Validate the BookChunk object before storing
            if not DataValidator.validate_book_chunk(book_chunk):
                skipped_count += 1
                continue

            # Store the chunk in the vector database
            chunk_id = self.retrieval_service.store_chunk(book_chunk)
            stored_chunk_ids.append(chunk_id)
            processed_count += 1

        return {
            "processed_count": processed_count,
            "skipped_count": skipped_count,
            "stored_chunk_ids": stored_chunk_ids,
            "status": "completed"
        }

    def embed_single_chunk(self, text: str, source_url: str, chapter: str, position: int) -> str:
        """
        Generate embedding for a single text chunk and store it.

        Args:
            text: The text content to embed
            source_url: The source URL of the content
            chapter: The chapter name/number
            position: The position in the chapter

        Returns:
            ID of the stored chunk
        """
        # Prepare raw data for validation
        raw_data = {
            "text": text,
            "source_url": source_url,
            "chapter": chapter,
            "position": position
        }

        # Validate the raw data
        if not DataValidator.validate_ingestion_data(raw_data):
            raise ValueError(f"Invalid data for chunk: {source_url}")

        book_chunk = BookChunk(
            text_content=text,
            source_url=source_url,
            chapter=chapter,
            position=position
        )

        # Validate the BookChunk object
        if not DataValidator.validate_book_chunk(book_chunk):
            raise ValueError(f"Invalid BookChunk for URL: {source_url}")

        chunk_id = self.retrieval_service.store_chunk(book_chunk)
        return chunk_id

    def validate_url(self, url: str) -> bool:
        """
        Validate that a URL is properly formatted.

        Args:
            url: The URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def chunk_text(self, text: str, max_tokens: int = 600) -> List[str]:
        """
        Split text into chunks of approximately max_tokens length.

        Args:
            text: The text to chunk
            max_tokens: Maximum number of tokens per chunk (approximated as words)

        Returns:
            List of text chunks
        """
        # Simple approach: split by sentences and group into chunks
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # Approximate token count as word count
            if len((current_chunk + " " + sentence).split()) > max_tokens and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def process_book_content(self, book_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process entire book content by chunking and embedding.

        Args:
            book_content: Dictionary containing book content with structure:
                         {
                           "title": "Book Title",
                           "chapters": [
                             {
                               "title": "Chapter Title",
                               "url": "Chapter URL",
                               "content": "Chapter content..."
                             }
                           ]
                         }

        Returns:
            Dictionary with processing results
        """
        from src.utils.logger import logger

        all_chunk_ids = []
        total_processed = 0
        total_skipped = 0

        chapters = book_content.get("chapters", [])
        logger.info("Starting book content processing", extra={
            "title": book_content.get("title", "Unknown"),
            "total_chapters": len(chapters)
        })

        for chapter_idx, chapter in enumerate(chapters):
            chapter_content = chapter.get("content", "")
            chapter_title = chapter.get("title", f"Chapter {chapter_idx + 1}")
            chapter_url = chapter.get("url", "")

            # Validate chapter data
            chapter_data = {
                "text": chapter_content,
                "source_url": chapter_url,
                "chapter": chapter_title,
                "position": 0  # Position will be set for individual chunks
            }

            if not DataValidator.validate_ingestion_data(chapter_data):
                logger.error("Invalid chapter data, skipping", extra={
                    "chapter_title": chapter_title,
                    "chapter_url": chapter_url,
                    "chapter_index": chapter_idx
                })
                total_skipped += len(self.chunk_text(chapter_content))  # Approximate number of chunks that would be skipped
                continue

            # Validate URL using our method
            if not self.validate_url(chapter_url):
                logger.error("Invalid URL for chapter, skipping", extra={
                    "chapter_title": chapter_title,
                    "chapter_url": chapter_url
                })
                continue

            # Chunk the chapter content
            text_chunks = self.chunk_text(chapter_content)

            # Process each chunk
            for position, chunk_text in enumerate(text_chunks, 1):
                if len(chunk_text.strip()) > 0:  # Skip empty chunks
                    try:
                        chunk_id = self.embed_single_chunk(
                            text=chunk_text,
                            source_url=chapter_url,
                            chapter=chapter_title,
                            position=position
                        )
                        all_chunk_ids.append(chunk_id)
                        total_processed += 1
                    except ValueError as e:
                        logger.error("Failed to embed chunk", extra={
                            "chapter_title": chapter_title,
                            "chapter_url": chapter_url,
                            "position": position,
                            "error": str(e)
                        })
                        total_skipped += 1
                        continue

        logger.info("Book content processing completed", extra={
            "processed_count": total_processed,
            "skipped_count": total_skipped,
            "stored_chunk_ids_count": len(all_chunk_ids)
        })

        return {
            "processed_count": total_processed,
            "skipped_count": total_skipped,
            "stored_chunk_ids": all_chunk_ids,
            "status": "completed",
            "message": f"Successfully processed {total_processed} text chunks from {len(book_content.get('chapters', []))} chapters, with {total_skipped} chunks skipped due to validation errors"
        }