import React from 'react';
import ChatWidget from '../components/ChatWidget';

const ChatWidgetWrapper = () => {
  // Get the current page URL to pass to the chat widget
  const currentUrl = typeof window !== 'undefined' ? window.location.href : '';

  return (
    <ChatWidget
      apiEndpoint={process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/v1'}
      bookUrl={currentUrl}
    />
  );
};

export default ChatWidgetWrapper;