# ADR-001: RAG Chatbot Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-21
- **Feature:** rag-chatbot-integration
- **Context:** Need to select a technology stack for implementing a RAG (Retrieval-Augmented Generation) chatbot that allows users to ask questions about book content with source citations. The system requires vector storage, embedding generation, AI-powered responses, and frontend integration with a Docusaurus-based book website.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Backend Stack:**
- Framework: FastAPI (Python 3.11) - for high-performance async API development
- Embeddings: Cohere embed-multilingual-v3.0 - for multilingual embedding generation
- Vector Database: Qdrant Cloud - for vector similarity search and storage
- Relational Database: Neon Serverless Postgres - for metadata and session storage
- AI Integration: OpenAI Agents SDK - for generating contextual answers
- Rate Limiting: Token bucket algorithm with Redis - for API protection

**Frontend Integration:**
- Pattern: Embedded chat widget in Docusaurus pages - for seamless book integration
- Components: React-based ChatWidget, TextSelector, CitationDisplay - for rich UI
- API Communication: RESTful JSON API - for simplicity and compatibility

## Consequences

### Positive

- Cohere's multilingual embedding model supports the requirement for multilingual question support
- Qdrant Cloud provides reliable vector search with good performance characteristics
- FastAPI provides excellent developer experience with built-in OpenAPI documentation
- The architecture cleanly separates concerns between embedding, retrieval, and generation
- Integration with Docusaurus allows users to ask questions without leaving book content
- Token bucket rate limiting provides smooth rate limiting with burst capacity

### Negative

- Dependency on multiple external APIs (Cohere, OpenAI, Qdrant) creates potential failure points
- Cohere embeddings may have higher costs compared to open-source alternatives
- Qdrant Cloud introduces vendor lock-in for the vector database component
- The architecture requires managing multiple services which increases operational complexity
- Text selection feature adds complexity to the frontend implementation

## Alternatives Considered

**Alternative Stack A: Open Source Stack**
- Framework: FastAPI with Sentence Transformers embeddings
- Vector Database: Self-hosted Chroma or Weaviate
- AI Integration: Open-source models (e.g., llama.cpp, Hugging Face)
- Why rejected: Would require more infrastructure management and potentially lower quality embeddings/answers

**Alternative Stack B: Different Cloud Providers**
- Embeddings: OpenAI text-embedding-ada-002 or Voyage AI
- Vector Database: Pinecone or Weaviate Cloud
- Why rejected: Cohere was specifically selected for multilingual capabilities; Qdrant was mentioned in initial requirements

**Alternative Stack C: Different Architecture Pattern**
- Separate standalone chat application vs embedded widget
- WebSocket streaming vs REST API
- Why rejected: Embedded widget maintains book context; REST API was simpler and sufficient for requirements

## References

- Feature Spec: specs/001-rag-chatbot-integration/spec.md
- Implementation Plan: specs/001-rag-chatbot-integration/plan.md
- Related ADRs: None
- Evaluator Evidence: specs/001-rag-chatbot-integration/research.md