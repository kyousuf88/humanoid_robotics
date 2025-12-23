import React from 'react';
import ChatWidget from './ChatWidget';

// Default theme Root component that wraps the entire app
function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}

export default Root;