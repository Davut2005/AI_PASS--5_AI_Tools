import React, { useState } from 'react';
import { aiAPI } from '../../services/api';
import './AITool.css';

interface ChatInterfaceProps {
  onCreditUpdate: () => void;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onCreditUpdate }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setError('');
    setLoading(true);

    try {
      const response = await aiAPI.chat(input);
      const assistantMessage: Message = { role: 'assistant', content: response.output_text };
      setMessages(prev => [...prev, assistantMessage]);
      onCreditUpdate();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-tool">
      <div className="tool-header">
        <h2>💬 AI Chat Assistant</h2>
        <p>Have a conversation with AI - 1 credit per message</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="chat-container">
        <div className="messages-area">
          {messages.length === 0 && (
            <div className="empty-state">
              <p>👋 Start a conversation! Ask me anything.</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>

        <form className="input-area" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;