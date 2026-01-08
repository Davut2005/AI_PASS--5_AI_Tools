import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import Sidebar from './Sidebar';
import ChatInterface from '../ai-tools/ChatInterface';
import TextSummarizer from '../ai-tools/TextSummarizer';
import ContentGenerator from '../ai-tools/ContentGenerator';
import CodeHelper from '../ai-tools/CodeHelper';
import TextAnalyzer from '../ai-tools/TextAnalyzer';
import CreditDisplay from './CreditDisplay';
import './Dashboard.css';

type ToolType = 'chat' | 'summarizer' | 'generator' | 'code-helper' | 'analyzer';

const Dashboard: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [selectedTool, setSelectedTool] = useState<ToolType>('chat');
  const [credits, setCredits] = useState(user?.credits || 0);

  useEffect(() => {
    if (user) {
      setCredits(user.credits);
    }
  }, [user]);

  const handleCreditUpdate = async () => {
    await refreshUser();
  };

  const renderTool = () => {
    switch (selectedTool) {
      case 'chat':
        return <ChatInterface onCreditUpdate={handleCreditUpdate} />;
      case 'summarizer':
        return <TextSummarizer onCreditUpdate={handleCreditUpdate} />;
      case 'generator':
        return <ContentGenerator onCreditUpdate={handleCreditUpdate} />;
      case 'code-helper':
        return <CodeHelper onCreditUpdate={handleCreditUpdate} />;
      case 'analyzer':
        return <TextAnalyzer onCreditUpdate={handleCreditUpdate} />;
      default:
        return <ChatInterface onCreditUpdate={handleCreditUpdate} />;
    }
  };

  return (
    <div className="dashboard">
      <Sidebar 
        selectedTool={selectedTool} 
        onSelectTool={(tool: string) => setSelectedTool(tool as ToolType)}
      />
      <div className="main-content">
        <div className="dashboard-header">
          <div className="user-info">
            <h2>Welcome, {user?.name}</h2>
            <span className="user-role">{user?.role}</span>
          </div>
          <CreditDisplay credits={credits} />
        </div>
        <div className="tool-container">
          {renderTool()}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;