# Quickstart: RAG Chatbot Integration

## Overview
This guide provides the essential steps to set up and run the RAG Chatbot Integration for the AI/Spec-Driven Book.

## Prerequisites
- Python 3.11+
- Docker (for local development)
- Access to Cohere API
- Access to OpenAI API
- Qdrant Cloud account
- Neon Postgres account

## Environment Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-name>
cd backend  # Navigate to the backend directory
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the backend directory with the following:

```env
COHERE_API_KEY=your_cohere_api_key
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_postgres_connection_string
SECRET_KEY=your_secret_key_for_session_management
DEBUG=true  # Set to false in production
```

## Running the Application

### 1. Backend Setup
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn cohere openai qdrant-client psycopg2-binary python-dotenv

# Run the backend server
uvicorn src.api.main:app --reload --port 8000
```

### 2. Initialize Vector Database
```bash
# Run the embedding script to process book content
python -m src.utils.scraper --url "https://your-book-url.com"
python -m src.services.embedding_service --process-all
```

### 3. Frontend Integration
The frontend components need to be integrated with the existing Docusaurus book website:

1. Copy the frontend components to the Docusaurus source
2. Add the chat widget to the book layout
3. Configure the API endpoint URL in the frontend

## API Testing

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main concept of the book?",
    "context_mode": "full_book"
  }'
```

### 3. Query Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning concepts",
    "top_k": 3,
    "min_relevance_score": 0.75
  }'
```

## Frontend Integration

### 1. Add Chat Widget to Docusaurus
Add the following to your Docusaurus layout:

```jsx
import ChatWidget from './path/to/ChatWidget';

// In your layout component
<ChatWidget
  apiEndpoint="http://localhost:8000"
  bookUrl={currentUrl}
/>
```

### 2. Enable Text Selection
The chat widget should detect text selection on the page and provide an option to ask questions about the selected text.

## Configuration Options

### 1. Chunking Parameters
- Default chunk size: 200-800 tokens
- Can be adjusted in `src/utils/chunker.py`

### 2. Rate Limiting
- Default: 100 requests/hour per session
- Configurable in `src/api/middleware/rate_limiter.py`

### 3. Relevance Threshold
- Default: 0.75 minimum relevance score
- Configurable in `src/services/retrieval_service.py`

## Troubleshooting

### Common Issues:

1. **API Keys Not Working**: Verify all API keys are correctly set in the environment variables
2. **Qdrant Connection**: Ensure the Qdrant URL and API key are correct
3. **Slow Response Times**: Check if the embedding process has completed for all book content
4. **Rate Limiting**: Verify the rate limiter is configured correctly

### Useful Commands:
```bash
# Check if all book content is embedded
python -c "from src.services.qdrant_service import QdrantService; print(QdrantService().count_chunks())"

# Test Cohere connection
python -c "import cohere; co = cohere.Client('your-key'); print(co.embed(texts=['test'], model='embed-multilingual-v3.0'))"

# Test OpenAI connection
python -c "import openai; openai.api_key='your-key'; print(openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'test'}], max_tokens=5))"
```

## Next Steps
1. Complete the embedding of all book content
2. Test the chat functionality with various questions
3. Integrate with the Docusaurus frontend
4. Deploy to production environment