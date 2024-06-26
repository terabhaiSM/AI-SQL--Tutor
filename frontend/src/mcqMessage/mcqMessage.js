// MCQMessage.js
import React, { useState } from 'react';
import './mcqMessage.css';

const MCQMessage = ({ question, options, onOptionSelect }) => {
    const [selectedOption, setSelectedOption] = useState(null);

    const handleOptionSelect = (option) => {
        setSelectedOption(option);
        onOptionSelect(option);
    };

    return (
        <div className="mcq-message">
            <p>{question}</p>
            <div className="mcq-options">
                {options.map((option, index) => (
                    <button
                        key={index}
                        className={`mcq-option ${selectedOption === option ? 'selected' : ''}`}
                        onClick={() => handleOptionSelect(option)}
                        disabled={selectedOption !== null}
                    >
                        {option}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default MCQMessage;
