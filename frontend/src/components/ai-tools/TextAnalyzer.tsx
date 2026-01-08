import React, { useState } from 'react';
import { aiAPI } from '../../services/api';
import './AITool.css';

interface TextAnalyzerProps {
  onCreditUpdate: () => void;
}

const TextAnalyzer: React.FC<TextAnalyzerProps> = ({ onCreditUpdate }) => {
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
      const response = await aiAPI.analyze(input);
      setOutput(response.output_text);
      onCreditUpdate();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-tool">
      <div className="tool-header">
        <h2>🔍 Text Analyzer</h2>
        <p>Analyze sentiment and extract key points - 2 credits</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="tool-form">
        <div className="form-section">
          <label>Enter text to analyze:</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste text for analysis..."
            rows={10}
            disabled={loading}
            required
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading || !input.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Text'}
        </button>

        {output && (
          <div className="output-section">
            <h3>Analysis Results:</h3>
            <div className="output-content">{output}</div>
          </div>
        )}
      </form>
    </div>
  );
};

export default TextAnalyzer;