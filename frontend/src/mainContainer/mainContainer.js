// MainContainer.js
import React, { useState } from 'react';
import Sidebar from '../sideBar/sidebar';
import './mainContainer.css';

const MainContainer = () => {
    const [activeTab, setActiveTab] = useState('steps');
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isCollapsed, setIsCollapsed] = useState(false);

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const handleSendMessage = () => {
        if (inputValue.trim() === '') return;

        const newMessage = {
            sender: 'user',
            text: inputValue,
        };

        setMessages([...messages, newMessage, { sender: 'ai', text: 'AI response here' }]);
        setInputValue('');
    };

    const handleToggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };

    return (
        <div className="main-container">
            <Sidebar 
                activeTab={activeTab} 
                onTabClick={handleTabClick} 
                messages={messages} 
                isCollapsed={isCollapsed}
                onToggle={handleToggleSidebar}
            />
            <div className={`chat-interface ${isCollapsed ? 'expanded' : ''}`}>
                <div className="chat-window">
                    {messages.map((message, index) => (
                        <div key={index} className={`chat-message ${message.sender}-message`}>
                            {message.text}
                        </div>
                    ))}
                </div>
                <div className="input-area">
                    <input 
                        type="text" 
                        className="input-box" 
                        placeholder="Type your message here..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                    />
                    <button className="send-button" onClick={handleSendMessage}>Send</button>
                </div>
            </div>
        </div>
    );
};

export default MainContainer;
