import React from 'react';
import ChatWidget from './components/ChatWidget';
import './theme/ChatWidgetWrapper.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Humanoid Robotics RAG Chatbot</h1>
      </header>
      <main>
        <ChatWidget />
      </main>
    </div>
  );
}

export default App;