# Data Model: RAG Chatbot Integration

## Entities

### BookChunk
Represents a segment of book content with text, source URL, chapter reference, and position in the book; used for embedding and retrieval.

**Fields**:
- `id`: UUID (primary key) - Unique identifier for the chunk
- `text_content`: Text (required) - The actual text content of the chunk (max 1000 words/tokens)
- `source_url`: URL (required) - URL of the source page in the Docusaurus book
- `chapter`: String (required) - Chapter or section name where this chunk appears
- `position`: Integer (required) - Sequential position of this chunk within the chapter
- `embedding`: Vector (required) - The vector embedding of the text content
- `metadata`: JSON - Additional metadata about the chunk
- `created_at`: DateTime (required) - Timestamp when chunk was created
- `updated_at`: DateTime - Timestamp when chunk was last updated

**Relationships**:
- One-to-many with UserSession (via selected_text reference)

### QueryResult
Contains the answer to a user's question along with source citations and relevance scores; returned to the frontend.

**Fields**:
- `id`: UUID (primary key) - Unique identifier for the query result
- `question`: Text (required) - The original user question
- `answer`: Text (required) - The generated answer from the chatbot
- `source_citations`: JSON Array (required) - List of source citations with URLs and relevance scores
- `relevance_score`: Float (required) - Overall relevance score (0.0 to 1.0)
- `retrieved_chunks`: Array of BookChunk references - The chunks used to generate the answer
- `query_timestamp`: DateTime (required) - When the query was made
- `session_id`: UUID - Reference to the user session that made this query

**Relationships**:
- Belongs to UserSession

### UserSession
Tracks the context of a user's interaction, particularly for selected-text questions that need to maintain focus on specific content.

**Fields**:
- `id`: UUID (primary key) - Unique identifier for the session
- `session_token`: String (required) - Token to identify the session (for rate limiting)
- `created_at`: DateTime (required) - When the session was created
- `last_activity`: DateTime (required) - Last interaction timestamp
- `selected_text`: Text (optional) - The currently selected text (for selected-text mode)
- `query_history`: Array of QueryResult references - History of queries in this session
- `rate_limit_remaining`: Integer (required) - Remaining rate limit requests for this session
- `rate_limit_reset`: DateTime (required) - When the rate limit will reset

**Relationships**:
- One-to-many with QueryResult
- One-to-many with BookChunk (via selected_text reference)

## Validation Rules

### BookChunk
- `text_content` must be between 200-800 tokens as specified in requirements
- `source_url` must be a valid URL from the book website
- `position` must be a positive integer
- `relevance_score` (if stored) must be between 0.0 and 1.0
- `embedding` must be a valid vector representation

### QueryResult
- `question` must not be empty
- `answer` must not be empty
- `relevance_score` must be between 0.0 and 1.0
- `source_citations` must contain at least one citation when answer is provided
- `retrieved_chunks` must contain at least one chunk when answer is provided

### UserSession
- `session_token` must be unique for rate limiting purposes
- `selected_text` (if present) must be limited to 1000 words/tokens maximum
- `rate_limit_remaining` must not be negative
- Session must be considered expired after 30 minutes of inactivity

## State Transitions

### UserSession
- `Active` → `Inactive`: When no activity for 30 minutes
- `Inactive` → `Active`: When user makes a new query
- `Active` → `RateLimited`: When rate limit is exceeded
- `RateLimited` → `Active`: When rate limit window resets

## Database Schema (PostgreSQL)

```sql
-- BookChunk table
CREATE TABLE book_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text_content TEXT NOT NULL,
    source_url VARCHAR(2048) NOT NULL,
    chapter VARCHAR(255) NOT NULL,
    position INTEGER NOT NULL,
    embedding vector(1024), -- Adjust dimension based on embedding model
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- UserSession table
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    selected_text TEXT,
    rate_limit_remaining INTEGER DEFAULT 100,
    rate_limit_reset TIMESTAMP WITH TIME ZONE,
    INDEX idx_session_token (session_token),
    INDEX idx_last_activity (last_activity)
);

-- QueryResult table
CREATE TABLE query_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source_citations JSONB NOT NULL,
    relevance_score FLOAT NOT NULL,
    query_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    session_id UUID REFERENCES user_sessions(id),
    INDEX idx_session_id (session_id),
    INDEX idx_query_timestamp (query_timestamp)
);

-- Indexes for performance
CREATE INDEX idx_book_chunks_chapter ON book_chunks(chapter);
CREATE INDEX idx_book_chunks_source_url ON book_chunks(source_url);
CREATE INDEX idx_book_chunks_position ON book_chunks(chapter, position);
```

## Vector Storage Schema (Qdrant)

```json
{
  "collection_name": "book_embeddings",
  "vectors": {
    "size": 1024,
    "distance": "Cosine"
  },
  "payload_schema": {
    "text_chunk_id": {
      "type": "keyword"
    },
    "source_url": {
      "type": "keyword"
    },
    "chapter": {
      "type": "keyword"
    },
    "position": {
      "type": "integer"
    },
    "metadata": {
      "type": "keyword"
    }
  }
}
```