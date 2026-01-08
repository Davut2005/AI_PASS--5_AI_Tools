import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <nav className="navbar">
        <h1 className="logo">AI-Pass</h1>
        <div className="nav-buttons">
          <button onClick={() => navigate('/login')} className="btn-secondary">
            Login
          </button>
          <button onClick={() => navigate('/register')} className="btn-primary">
            Get Started
          </button>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <h1>All AI Tools in One Platform</h1>
          <p>
            Access ChatGPT, text analysis, content generation, and more AI tools
            under one subscription with unified credit-based billing.
          </p>
          <button onClick={() => navigate('/register')} className="btn-hero">
            Start Free Trial
          </button>
        </div>
      </section>

      <section className="features">
        <h2>Why Choose AI-Pass?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h3>AI Chat</h3>
            <p>Conversational AI powered by advanced language models</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Text Summarizer</h3>
            <p>Instantly summarize long documents and articles</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">✨</div>
            <h3>Content Generator</h3>
            <p>Create high-quality content for any topic</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💻</div>
            <h3>Code Helper</h3>
            <p>Get programming assistance and code examples</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Text Analyzer</h3>
            <p>Analyze sentiment and extract key insights</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Credit System</h3>
            <p>Pay only for what you use with our flexible credits</p>
          </div>
        </div>
      </section>

      <footer className="footer">
        <p>&copy; 2024 AI-Pass. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default LandingPage;