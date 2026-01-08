import React from 'react';
import './CreditDisplay.css';

interface CreditDisplayProps {
  credits: number;
}

const CreditDisplay: React.FC<CreditDisplayProps> = ({ credits }) => {
  const getStatusClass = () => {
    if (credits >= 50) return 'status-good';
    if (credits >= 20) return 'status-warning';
    return 'status-low';
  };

  return (
    <div className={`credit-display ${getStatusClass()}`}>
      <div className="credit-icon">⚡</div>
      <div className="credit-info">
        <span className="credit-label">Available Credits</span>
        <span className="credit-amount">{credits}</span>
      </div>
    </div>
  );
};

export default CreditDisplay;