import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

// API client implementation for use in Docusaurus
class ApiClient {
  constructor(baseURL) {
    // Check if process is available (for React app environment) or use default
    const defaultURL = typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL
      ? process.env.REACT_APP_API_BASE_URL
      : 'http://localhost:8000/v1'; // Default to the backend API
    this.baseURL = baseURL || defaultURL;
  }

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

  async initSession(sessionContext = null) {
    const body = sessionContext ? { session_context: sessionContext } : {};
    return this.request('/session/init', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async askQuestion(questionData) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify(questionData),
    });
  }
}

const apiClient = new ApiClient();

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [contextMode, setContextMode] = useState('full_book');
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Initialize session when component mounts
  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await apiClient.initSession();
        setSessionId(response.data.session_id);
      } catch (error) {
        console.error('Failed to initialize session:', error);
      }
    };

    initSession();
  }, []);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
      selectedText: contextMode === 'selected_text' ? selectedText : null
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request payload
      const requestPayload = {
        question: inputValue,
        context_mode: contextMode,
        session_id: sessionId
      };

      // Include selected text if in selected_text mode
      if (contextMode === 'selected_text' && selectedText) {
        requestPayload.selected_text = selectedText;
      }

      // Call the API
      const response = await apiClient.askQuestion(requestPayload);

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: response.data.answer,
        sender: 'bot',
        citations: response.data.source_citations,
        relevance_score: response.data.relevance_score,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting response:', error);

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error while processing your question. Please try again.',
        sender: 'bot',
        isError: true,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      // Validate the selected text
      const wordCount = selectedText.split(/\s+/).length;
      if (wordCount > 1000) {
        alert(`Selected text is too long (${wordCount} words). Please select fewer than 1000 words.`);
        return;
      }

      setSelectedText(selectedText);
      setContextMode('selected_text');

      // Optionally add a message to the chat indicating text selection
      const selectionMessage = {
        id: Date.now(),
        text: `I'll answer your questions based on the selected text (${wordCount} words): "${selectedText.substring(0, 100)}${selectedText.length > 100 ? '...' : ''}"`,
        sender: 'system',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, selectionMessage]);
    }
  };

  const toggleWidget = () => {
    setIsOpen(!isOpen);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="chat-widget">
      {/* Floating button to open/close chat */}
      <button className="chat-toggle-button" onClick={toggleWidget}>
        {isOpen ? 'Close Chat' : 'Ask Book'}
      </button>

      {/* Chat container */}
      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <h3>Book Assistant</h3>
            <div className="chat-controls">
              <button onClick={clearChat} className="clear-chat-btn" title="Clear chat">
                ✕
              </button>
              <button onClick={toggleWidget} className="close-chat-btn" title="Close">
                −
              </button>
            </div>
          </div>

          <div className="chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender}-message`}
              >
                <div className="message-content">
                  {message.sender === 'bot' && message.isError ? (
                    <div className="error-message">
                      {message.text}
                    </div>
                  ) : (
                    <>
                      <div className="message-text">{message.text}</div>
                      {message.citations && message.citations.length > 0 && (
                        <div className="citations">
                          <strong>Sources:</strong>
                          <ul>
                            {message.citations.map((citation, index) => (
                              <li key={index}>
                                <span>{citation.title}</span>
                                <span className="relevance-score">
                                  (Relevance: {(citation.relevance_score * 100).toFixed(1)}%)
                                </span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </>
                  )}
                </div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content">
                  <div className="loading-indicator">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-input-form" onSubmit={handleSubmit}>
            <div className="context-mode-selector">
              <label>
                <input
                  type="radio"
                  value="full_book"
                  checked={contextMode === 'full_book'}
                  onChange={() => setContextMode('full_book')}
                />
                Full Book
              </label>
              <label>
                <input
                  type="radio"
                  value="selected_text"
                  checked={contextMode === 'selected_text'}
                  onChange={() => {
                    if (selectedText) {
                      setContextMode('selected_text');
                    } else {
                      alert('Please select text from the page first');
                    }
                  }}
                />
                Selected Text
              </label>
            </div>

            {contextMode === 'selected_text' && selectedText && (
              <div className="selected-text-preview">
                <div className="selected-text-header">
                  <strong>Selected Text:</strong>
                  <span className="word-count">({selectedText.split(/\s+/).length} words)</span>
                </div>
                <div className="selected-text-content">
                  "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
                </div>
              </div>
            )}

            <div className="input-container">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask a question about the book..."
                disabled={isLoading}
                autoFocus
              />
              <button type="submit" disabled={isLoading || !inputValue.trim()}>
                {isLoading ? 'Sending...' : 'Ask'}
              </button>
            </div>
          </form>

          <div className="chat-footer">
            <button onClick={handleTextSelection} className="select-text-btn">
              Select Text
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;