// Sidebar.js
import React from 'react';
import './sidebar.css';

const Sidebar = ({ activeTab, onTabClick, messages, isCollapsed, onToggle }) => {
    return (
        <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            <button className="toggle-button" onClick={onToggle}>
                {isCollapsed ? '>' : '<'}
            </button>
            {!isCollapsed && (
                <>
                    <div className="tabs">
                        <button
                            className={`tab-button ${activeTab === 'steps' ? 'active' : ''}`}
                            onClick={() => onTabClick('steps')}
                        >
                            Steps
                        </button>
                        <button
                            className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
                            onClick={() => onTabClick('history')}
                        >
                            History
                        </button>
                    </div>
                    <div className="tab-content">
                        {activeTab === 'steps' && (
                            <div className="steps-content">
                                {/* Steps or guidelines content */}
                                <p>Step 1: Do this...</p>
                                <p>Step 2: Do that...</p>
                            </div>
                        )}
                        {activeTab === 'history' && (
                            <div className="history-content">
                                {/* Previous conversation history */}
                                {messages.map((message, index) => (
                                    <div key={index} className={`chat-message ${message.sender}-message`}>
                                        {message.text}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </>
            )}
        </div>
    );
};

export default Sidebar;
