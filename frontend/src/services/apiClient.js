// API client for the RAG Chatbot
class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL || process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/v1';
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      // Check if response is ok (status 2xx)
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Health check endpoint
  async healthCheck() {
    return this.request('/health', {
      method: 'GET',
    });
  }

  // Initialize a new session
  async initSession(sessionContext = null) {
    const body = sessionContext ? { session_context: sessionContext } : {};

    return this.request('/session/init', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  // Ask a question to the chatbot
  async askQuestion(questionData) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify(questionData),
    });
  }

  // Query the vector database directly
  async queryVectorDB(queryData) {
    return this.request('/query', {
      method: 'POST',
      body: JSON.stringify({
        question: queryData.question,
        context_mode: queryData.context_mode || 'full_book',
        selected_text: queryData.selected_text,
        session_id: queryData.session_id
      }),
    });
  }

  // Get rate limit information from response headers
  getRateLimitInfo(response) {
    return {
      limit: response.headers.get('X-RateLimit-Limit'),
      remaining: response.headers.get('X-RateLimit-Remaining'),
      reset: response.headers.get('X-RateLimit-Reset'),
    };
  }
}

// Create a singleton instance
const apiClient = new ApiClient();

export { apiClient, ApiClient };