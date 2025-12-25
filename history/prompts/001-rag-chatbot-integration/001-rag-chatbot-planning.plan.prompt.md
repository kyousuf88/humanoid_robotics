---
id: 001
title: rag-chatbot-planning
stage: plan
date: 2025-12-21
surface: agent
model: claude-haiku-4-5-20251001
feature: rag-chatbot-integration
branch: 001-rag-chatbot-integration
user: user
command: /sp.plan
labels: [rag, chatbot, planning, architecture]
links:
  spec: specs/001-rag-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-integration/spec.md
  - specs/001-rag-chatbot-integration/plan.md
  - specs/001-rag-chatbot-integration/research.md
  - specs/001-rag-chatbot-integration/data-model.md
  - specs/001-rag-chatbot-integration/contracts/api-contract.yaml
  - specs/001-rag-chatbot-integration/quickstart.md
tests:
  - null
---

## Prompt

```
/sp.plan -- RAG Chatbot System P
## Architecture Sketch
- **Frontend (Docusaurus Book Website)**
  - User selects text → Sends selected passage as query
  - Chat UI embedded inside the website (iframe or React integration)

- **Backend API (FastAPI)**
  - Endpoints:
    - `/embed` – generate embeddings using Cohere
    - `/query` – query Qdrant + return context chunks
    - `/chat` – OpenAI Agents SDK → final answer
  - Neon Postgres → store metadata and chat logs

- **Vector Store (Qdrant Cloud Free Tier)**
  - Collection: `book_embeddings`
  - Schema: `id`, `text_chunk`, `embedding`, `metadata {chapter, url, section}`

- **Agent Layer**
  - OpenAI Agent that includes:
    - Retrieval tool (Qdrant search)
    - Book-context grounding prompt
    - Safety + hallucination guardrails

- **Workflow**
  1. Deploy website → scrape → chunk → embed
  2. Store embeddings in Qdrant
  3. Test FastAPI pipeline
  4. Build retrieval-enabled agent
  5. Integrate backeOptions: Cohere, OpenAI, Voyage
   - Tradeoffs: quality vs cost vs multilingual ability

2. **Chunking Strategy**
   - Options: Paragraph-based, semantic splitter
   - Tradeoffs: coherence vs retrieval granularity

3. **Retrieval Method**
   - Dense vs hybrid (dense + keyword)

4. **Hosting**
   - Qdrant Cloud Free vs self-hosted Qdrant
   - FastAPI (local dev) vs deployment target

5. **Integration Pattern**
   - REST endpoints vs WebSocket streaming

---

## Testing Strategy

### Unit Tests
- Chunker
- Embedding generator
- Qdrant insert + query
- Agent tool correctness

### Pipeline Tests
- Full pipeline:
  `Website → Scraper → Chunker → Embeddings → Qdrant → Agent → UI`
- Validate extraction on 20+ random sections
- Ensure selected-text mode works flawlessly

### Acceptance Criteria
- 95%+ retrieval precision
- No hallucinations (grounded answers only)
- Chatbot loads and works inside Docusaurus
- API latency under 3 seconds
```

## Response snapshot

The planning workflow for the RAG Chatbot Integration feature was executed successfully. The existing planning artifacts were reviewed and are comprehensive:

1. **Feature Specification** (spec.md): Complete user stories and requirements for the RAG chatbot, including:
   - Book-wide question answering (P1)
   - Selected text question answering (P2)
   - Interactive chat interface (P3)
   - 21 functional requirements (FR-001 to FR-021)
   - 8 measurable success criteria (SC-001 to SC-008)

2. **Implementation Plan** (plan.md): Detailed technical approach with:
   - Backend (FastAPI) and frontend (Docusaurus integration) architecture
   - Technology stack: Python 3.11, FastAPI, OpenAI Agents SDK, Cohere, Qdrant, Neon Postgres
   - Performance goals: 800ms response time, 300ms Qdrant retrieval
   - Project structure with separate backend/frontend components

3. **Research** (research.md): Technology decisions documented:
   - Cohere embed-multilingual-v3.0 for embeddings
   - Qdrant Cloud for vector storage
   - FastAPI for backend framework
   - Semantic chunking strategy (200-800 tokens)
   - Neon Serverless Postgres for metadata
   - Token bucket rate limiting with Redis

4. **Data Model** (data-model.md): Three main entities defined:
   - BookChunk: Text content with source metadata and embeddings
   - QueryResult: AI-generated answers with source citations
   - UserSession: Session tracking with rate limiting

5. **API Contract** (contracts/api-contract.yaml): Complete API specification:
   - POST /chat: Process user questions with AI-generated answers
   - POST /query: Direct vector database queries
   - POST /embed: Generate and store embeddings
   - GET /health: Health check with dependency status
   - POST /session/init: Rate-limited session management

6. **Quickstart Guide** (quickstart.md): Setup and deployment instructions:
   - Environment setup with required API keys
   - Backend installation and run commands
   - Frontend integration with Docusaurus
   - API testing examples
   - Configuration options and troubleshooting

## Outcome

- ✅ Impact: Complete planning artifacts exist for RAG Chatbot Integration
- 🧪 Tests: No tests run during this planning review
- 📁 Files: All planning artifacts are comprehensive and ready for implementation
- 🔁 Next prompts: Ready to proceed with task generation and implementation
- 🧠 Reflection: The planning phase is complete and thorough, with all necessary design decisions made

## Evaluation notes (flywheel)

- Failure modes observed: None - planning is complete and comprehensive
- Graders run and results (PASS/FAIL): N/A for planning review
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation with /sp.tasks