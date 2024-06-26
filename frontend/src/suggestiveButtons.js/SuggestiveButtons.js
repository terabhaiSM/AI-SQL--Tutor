// SuggestiveButtons.js
import React from 'react';
import './SuggestiveButtons.css';

const SuggestiveButtons = ({ suggestions, onSuggestionClick }) => {
    return (
        <div className="suggestive-buttons">
            {suggestions.map((suggestion, index) => (
                <button
                    key={index}
                    className="suggestive-button"
                    onClick={() => onSuggestionClick(suggestion)}
                >
                    {suggestion}
                </button>
            ))}
        </div>
    );
};

export default SuggestiveButtons;
