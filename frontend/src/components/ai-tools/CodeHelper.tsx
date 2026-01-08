import React, { useState } from 'react';
import { aiAPI } from '../../services/api';
import './AITool.css';

interface CodeHelperProps {
  onCreditUpdate: () => void;
}

const CodeHelper: React.FC<CodeHelperProps> = ({ onCreditUpdate }) => {
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
      const response = await aiAPI.codeHelp(input);
      setOutput(response.output_text);
      onCreditUpdate();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get code help');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-tool">
      <div className="tool-header">
        <h2>💻 Code Helper</h2>
        <p>Get help with programming questions - 2 credits</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="tool-form">
        <div className="form-section">
          <label>Ask a coding question:</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., How do I implement a binary search in Python?"
            rows={6}
            disabled={loading}
            required
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading || !input.trim()}>
          {loading ? 'Processing...' : 'Get Help'}
        </button>

        {output && (
          <div className="output-section">
            <h3>Answer:</h3>
            <div className="output-content code-output">
              <pre>{output}</pre>
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default CodeHelper;