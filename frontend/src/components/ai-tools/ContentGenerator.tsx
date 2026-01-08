import React, { useState } from 'react';
import { aiAPI } from '../../services/api';
import './AITool.css';

interface ContentGeneratorProps {
  onCreditUpdate: () => void;
}

const ContentGenerator: React.FC<ContentGeneratorProps> = ({ onCreditUpdate }) => {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    setError('');
    setLoading(true);
    setOutput('');

    try {
      const response = await aiAPI.generate(input);
      setOutput(response.output_text);
      onCreditUpdate();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-tool">
      <div className="tool-header">
        <h2>✨ Content Generator</h2>
        <p>Generate comprehensive articles and content - 3 credits</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="tool-form">
        <div className="form-section">
          <label>Enter topic or title:</label>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., The future of artificial intelligence"
            disabled={loading}
            required
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading || !input.trim()}>
          {loading ? 'Generating...' : 'Generate Content'}
        </button>

        {output && (
          <div className="output-section">
            <h3>Generated Content:</h3>
            <div className="output-content">{output}</div>
          </div>
        )}
      </form>
    </div>
  );
};

export default ContentGenerator;