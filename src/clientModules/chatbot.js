import React from 'react';
import ReactDOM from 'react-dom/client';
import Chatbot from '../components/Chatbot';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

if (ExecutionEnvironment.canUseDOM) {
  // Wait for DOM to be ready
  window.addEventListener('DOMContentLoaded', () => {
    // Create a container for the chatbot
    const chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'chatbot-root';
    document.body.appendChild(chatbotContainer);

    // Mount the chatbot
    const root = ReactDOM.createRoot(chatbotContainer);
    root.render(<Chatbot />);
  });
}
