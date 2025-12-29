import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    const question = inputValue.trim();
    if (!question) return;

    // Add user message
    setMessages((prev) => [...prev, { text: `You: ${question}`, type: 'user' }]);
    setInputValue('');

    try {
      const res = await fetch('https://abdul123233-my-book.hf.space/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { text: `Bot: ${data.answer}`, type: 'bot' }]);
    } catch (err) {
      console.error('Error:', err);
      setMessages((prev) => [
        ...prev,
        { text: 'Bot: Backend not reachable. Make sure backend is running on port 8000!', type: 'bot' },
      ]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <>
      {/* Chatbot Icon */}
      <div className={styles.chatbotIcon} onClick={() => setIsOpen(true)} title="Ask about the book">
        💬
      </div>

      {/* Chatbot Box */}
      {isOpen && (
        <div className={styles.chatbotBox}>
          <div className={styles.chatHeader}>
            Book Chatbot
            <span className={styles.closeBtn} onClick={() => setIsOpen(false)}>
              ✖
            </span>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 && (
              <div className={styles.welcomeMessage}>
                👋 Hi! Ask me anything about Physical AI & Humanoid Robotics!
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} className={msg.type === 'user' ? styles.userMessage : styles.botMessage}>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInput}>
            <input
              type="text"
              placeholder="Ask about the book..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
    </>
  );
}
