/**
 * Header component - Application navigation
 */

import React from 'react';
import '../styles/components.css';

interface HeaderProps {
  currentPage: 'study' | 'vocabulary' | 'progress';
  onNavigate: (page: 'study' | 'vocabulary' | 'progress') => void;
}

export const Header: React.FC<HeaderProps> = ({ currentPage, onNavigate }) => {
  return (
    <header className="app-header">
      <div className="header-container">
        <div className="app-title">
          <h1>🌍 Language Learning Framework</h1>
          <p className="subtitle">Interactive learning with spaced repetition</p>
        </div>

        <nav className="main-nav">
          <button
            className={`nav-btn ${currentPage === 'study' ? 'active' : ''}`}
            onClick={() => onNavigate('study')}
          >
            📚 Study
          </button>
          <button
            className={`nav-btn ${currentPage === 'vocabulary' ? 'active' : ''}`}
            onClick={() => onNavigate('vocabulary')}
          >
            📝 Vocabulary
          </button>
          <button
            className={`nav-btn ${currentPage === 'progress' ? 'active' : ''}`}
            onClick={() => onNavigate('progress')}
          >
            📊 Progress
          </button>
        </nav>
      </div>
    </header>
  );
};
