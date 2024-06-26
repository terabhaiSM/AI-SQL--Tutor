// MainContainer.js
import React, { useState, useEffect } from 'react';
import Sidebar from '../sideBar/sidebar';
import './mainContainer.css';
import MCQMessage from '../mcqMessage/mcqMessage';
import SuggestiveButtons from '../suggestiveButtons.js/SuggestiveButtons';

const MainContainer = () => {
    const [activeTab, setActiveTab] = useState('steps');
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isCollapsed, setIsCollapsed] = useState(false);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/chat_history')
            .then(response => response.json())
            .then(data => {
                setMessages(data.history);
            });
    }, []);

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const handleSendMessage = () => {
        if (inputValue.trim() === '') return;

        const newMessage = {
            sender: 'user',
            text: inputValue,
        };

        // Send user message to backend
        fetch('http://127.0.0.1:5000/api/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: inputValue })
        })
        .then(response => response.json())
        .then(data => {
            const aiMessage = {
                sender: 'assistant',
                text: data.message
            };
            setMessages([...messages, newMessage, aiMessage]);

            if (data.suggestions) {
                setMessages(prevMessages => [
                    ...prevMessages,
                    {
                        sender: 'assistant',
                        type: 'suggestions',
                        suggestions: data.suggestions
                    }
                ]);
            }

            setInputValue('');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    const handleToggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };

    const handleOptionSelect = (option) => {
        // Handle the selected option here
        console.log('Selected option:', option);
    };

    const handleSuggestionClick = (suggestion) => {
        // Send question type to backend and fetch the question
        fetch('http://127.0.0.1:5000/api/generate_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question_type: suggestion.includes('MCQ') ? 'mcq' : 'descriptive' })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            data = JSON.parse(data.question);
            console.log(data);
            const newQuestion = {
                sender: 'assistant',
                type: data.type,
                text: data.question,
                options: data.type === 'mcq' ? data.options : {},
                correctAnswer: data.correctAnswer
            };
            setMessages(prevMessages => [...prevMessages, newQuestion]);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    const handleEvaluationComplete = () => {
        setMessages(prevMessages => [
            ...prevMessages,
            {
                sender: 'assistant',
                type: 'suggestions',
                suggestions: ['Generate an MCQ question', 'Generate a descriptive question']
            }
        ]);
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
                    {messages.map((message, index) => {
                        if (message.type === 'mcq') {
                            return (
                                <MCQMessage
                                    key={index}
                                    question={message.text}
                                    options={message.options}
                                    onOptionSelect={handleOptionSelect}
                                    correctAnswer= {message.correctAnswer}
                                    onEvaluationComplete={handleEvaluationComplete}
                                />
                            );
                        } else if (message.type === 'suggestions') {
                            return (
                                <div key={index} className="chat-message ai-message">
                                    <div>{message.text}</div>
                                    <SuggestiveButtons 
                                        suggestions={message.suggestions} 
                                        onSuggestionClick={handleSuggestionClick} 
                                    />
                                </div>
                            );
                        } else {
                            return (
                                <div key={index} className={`chat-message ${message.sender}-message`}>
                                    {message.text}
                                </div>
                            );
                        }
                    })}
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


