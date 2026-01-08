import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';


interface SidebarProps {
  selectedTool: string;
  onSelectTool: (tool: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ selectedTool, onSelectTool }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const tools = [
    { id: 'chat', name: 'AI Chat', icon: '💬', credits: 1 },
    { id: 'summarizer', name: 'Text Summarizer', icon: '📝', credits: 2 },
    { id: 'generator', name: 'Content Generator', icon: '✨', credits: 3 },
    { id: 'code-helper', name: 'Code Helper', icon: '💻', credits: 2 },
    { id: 'analyzer', name: 'Text Analyzer', icon: '🔍', credits: 2 },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>AI-Pass</h1>
        <p className="tagline">All AI Tools in One Place</p>
      </div>

      <div className="tools-section">
        <h3>AI Tools</h3>
        <div className="tools-list">
          {tools.map((tool) => (
            <button
              key={tool.id}
              className={`tool-item ${selectedTool === tool.id ? 'active' : ''}`}
              onClick={() => onSelectTool(tool.id)}
            >
              <span className="tool-icon">{tool.icon}</span>
              <div className="tool-info">
                <span className="tool-name">{tool.name}</span>
                <span className="tool-credits">{tool.credits} credits</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <button className="logout-btn" onClick={handleLogout}>
          🚪 Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;