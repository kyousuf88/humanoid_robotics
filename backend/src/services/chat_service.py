from typing import List, Dict, Any, Optional
from openai import OpenAI
from src.models.query_result import QueryResult, SourceCitation
from src.services.retrieval_service import RetrievalService
from src.utils.config import settings
from src.utils.cache_service import cache_service
from datetime import datetime
import uuid


class ChatService:
    """
    Service for handling chat interactions using OpenAI Agents SDK.
    Processes user questions and generates contextual answers with source citations.
    """

    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.retrieval_service = RetrievalService()

    def generate_answer(
        self,
        question: str,
        context_mode: str = "full_book",
        selected_text: Optional[str] = None,
        top_k: int = 5,
        min_relevance_score: float = 0.75
    ) -> QueryResult:
        """
        Generate an answer to the user's question using retrieved context.

        Args:
            question: The user's question
            context_mode: "full_book" or "selected_text"
            selected_text: Text selected by user (for selected_text mode)
            top_k: Number of context chunks to retrieve
            min_relevance_score: Minimum similarity threshold

        Returns:
            QueryResult object with answer and citations
        """
        # Check if response is cached
        cached_response = cache_service.get_cached_response(question, context_mode, selected_text)
        if cached_response:
            # Return cached result as a QueryResult object
            return QueryResult(
                question=cached_response.get('question', question),
                answer=cached_response.get('answer', ''),
                source_citations=cached_response.get('source_citations', []),
                relevance_score=cached_response.get('relevance_score', 0.0),
                retrieved_chunks=cached_response.get('retrieved_chunks', [])
            )

        # Retrieve relevant chunks based on context mode
        if context_mode == "selected_text" and selected_text:
            # In selected text mode, we want to focus on content related to the selected text
            retrieved_chunks = self.retrieval_service.retrieve_chunks_by_selected_text(
                selected_text,
                top_k=top_k,
                min_relevance_score=min_relevance_score
            )
        else:
            # In full book mode, search across the entire book
            retrieved_chunks = self.retrieval_service.retrieve_chunks(
                question,
                top_k=top_k,
                min_relevance_score=min_relevance_score
            )

        # Format the context from retrieved chunks
        context_str = self._format_context(retrieved_chunks)

        # Generate the answer using OpenAI
        answer = self._generate_with_openai(question, context_str)

        # Create source citations
        citations = self._create_citations(retrieved_chunks)

        # Calculate relevance score (average of all chunk scores)
        relevance_score = self._calculate_relevance_score(retrieved_chunks)

        # Create and return the QueryResult
        query_result = QueryResult(
            question=question,
            answer=answer,
            source_citations=citations,
            relevance_score=relevance_score,
            retrieved_chunks=[uuid.UUID(chunk.get('id', str(uuid.uuid4()))) for chunk in retrieved_chunks if chunk.get('id')]
        )

        # Cache the response for future requests
        cache_service.cache_response(
            question=question,
            context_mode=context_mode,
            response={
                "question": query_result.question,
                "answer": query_result.answer,
                "source_citations": query_result.source_citations,
                "relevance_score": query_result.relevance_score,
                "retrieved_chunks": query_result.retrieved_chunks
            },
            selected_text=selected_text
        )

        return query_result

    def generate_answer_with_context_preservation(
        self,
        question: str,
        context_mode: str = "full_book",
        selected_text: Optional[str] = None,
        previous_context: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        min_relevance_score: float = 0.75
    ) -> QueryResult:
        """
        Generate an answer while preserving context for follow-up questions.

        Args:
            question: The user's question
            context_mode: "full_book" or "selected_text"
            selected_text: Text selected by user (for selected_text mode)
            previous_context: Context from previous interactions
            top_k: Number of context chunks to retrieve
            min_relevance_score: Minimum similarity threshold

        Returns:
            QueryResult object with answer and citations
        """
        # For context preservation, we don't want to cache responses as they're more dynamic
        # Check if response is cached (only for simple cases without previous context)
        if not previous_context:
            cached_response = cache_service.get_cached_response(question, context_mode, selected_text)
            if cached_response:
                # Return cached result as a QueryResult object
                return QueryResult(
                    question=cached_response.get('question', question),
                    answer=cached_response.get('answer', ''),
                    source_citations=cached_response.get('source_citations', []),
                    relevance_score=cached_response.get('relevance_score', 0.0),
                    retrieved_chunks=cached_response.get('retrieved_chunks', [])
                )

        # If in selected text mode and we have previous context, maintain that context
        if context_mode == "selected_text" and selected_text:
            # Use the selected text as the primary context
            retrieved_chunks = self.retrieval_service.retrieve_chunks_by_selected_text(
                selected_text,
                top_k=top_k,
                min_relevance_score=min_relevance_score
            )

            # If we have previous context, we can enhance the current context
            if previous_context:
                # For follow-up questions, we can use the previous selected text if no new selection
                selected_text = previous_context.get('selected_text', selected_text)
        else:
            # In full book mode, search across the entire book
            retrieved_chunks = self.retrieval_service.retrieve_chunks(
                question,
                top_k=top_k,
                min_relevance_score=min_relevance_score
            )

        # Format the context from retrieved chunks
        context_str = self._format_context(retrieved_chunks)

        # Include previous context if available
        if previous_context and previous_context.get('previous_answer'):
            context_str = (
                f"Previous context:\n{previous_context['previous_answer']}\n\n"
                f"New context:\n{context_str}\n\n"
                f"Question: {question}"
            )
        else:
            context_str = f"{context_str}\n\nQuestion: {question}"

        # Generate the answer using OpenAI
        answer = self._generate_with_openai(question, context_str)

        # Create source citations
        citations = self._create_citations(retrieved_chunks)

        # Calculate relevance score (average of all chunk scores)
        relevance_score = self._calculate_relevance_score(retrieved_chunks)

        # Create and return the QueryResult
        query_result = QueryResult(
            question=question,
            answer=answer,
            source_citations=citations,
            relevance_score=relevance_score,
            retrieved_chunks=[uuid.UUID(chunk.get('id', str(uuid.uuid4()))) for chunk in retrieved_chunks if chunk.get('id')]
        )

        # Cache the response only if there's no previous context (simple Q&A)
        if not previous_context:
            cache_service.cache_response(
                question=question,
                context_mode=context_mode,
                response={
                    "question": query_result.question,
                    "answer": query_result.answer,
                    "source_citations": query_result.source_citations,
                    "relevance_score": query_result.relevance_score,
                    "retrieved_chunks": query_result.retrieved_chunks
                },
                selected_text=selected_text
            )

        return query_result

    def _format_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Format retrieved chunks into a context string for the LLM.

        Args:
            retrieved_chunks: List of retrieved chunks

        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return "No relevant information found in the book."

        context_parts = ["Here is the relevant information from the book:"]
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(
                f"Source {i} (Chapter: {chunk['chapter']}, Position: {chunk['position']}):\n"
                f"{chunk['text']}\n"
                f"Source URL: {chunk['source_url']}\n"
            )

        return "\n".join(context_parts)

    def _generate_with_openai(self, question: str, context: str) -> str:
        """
        Generate an answer using OpenAI's API.

        Args:
            question: The user's question
            context: The context to use for answering

        Returns:
            Generated answer
        """
        prompt = (
            f"Based on the following context from the book, please answer the user's question. "
            f"Provide a comprehensive answer that directly addresses the question. "
            f"If the answer cannot be found in the context, say so clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"Answer:"
        )

        try:
            response = self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided book content. Always provide accurate answers based only on the given context. If the answer is not in the context, clearly state that the information is not available in the provided text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3,
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            # In case of an error, return a helpful message
            return f"Sorry, I encountered an error while processing your question: {str(e)}"

    def _create_citations(self, retrieved_chunks: List[Dict[str, Any]]) -> List[SourceCitation]:
        """
        Create source citations from retrieved chunks.

        Args:
            retrieved_chunks: List of retrieved chunks

        Returns:
            List of SourceCitation objects
        """
        citations = []
        for chunk in retrieved_chunks:
            citation = SourceCitation(
                url=chunk.get("source_url", ""),
                title=f"Chapter: {chunk.get('chapter', 'Unknown')}, Position: {chunk.get('position', 0)}",
                relevance_score=chunk.get("relevance_score", 0.0)
            )
            citations.append(citation)

        # If no citations were created, create a default citation indicating no sources found
        if not citations:
            citations.append(SourceCitation(
                url="",
                title="No relevant sources found in the book",
                relevance_score=0.0
            ))

        return citations

    def _calculate_relevance_score(self, retrieved_chunks: List[Dict[str, Any]]) -> float:
        """
        Calculate the overall relevance score as the average of all chunk scores.

        Args:
            retrieved_chunks: List of retrieved chunks

        Returns:
            Average relevance score
        """
        if not retrieved_chunks:
            return 0.0

        total_score = sum(chunk.get("relevance_score", 0.0) for chunk in retrieved_chunks)
        return total_score / len(retrieved_chunks)

    def handle_multilingual_question(
        self,
        question: str,
        context_mode: str = "full_book",
        selected_text: Optional[str] = None,
        target_language: Optional[str] = None
    ) -> QueryResult:
        """
        Handle a question in a different language than the book content.
        The response will be in the book's original language or specified target language.

        Args:
            question: The user's question (potentially in different language)
            context_mode: "full_book" or "selected_text"
            selected_text: Text selected by user (for selected_text mode)
            target_language: Optional target language for the response

        Returns:
            QueryResult object with answer in book's original language or target language
        """
        # For now, we handle multilingual questions by using the standard generate_answer method
        # In the future, we could add language detection and translation capabilities
        result = self.generate_answer(question, context_mode, selected_text)

        # If a target language is specified and it differs from the book's language,
        # we could implement translation here
        if target_language and target_language != settings.book_language:
            # This would require a translation service in a full implementation
            # For now, we return the result as is
            pass

        return result