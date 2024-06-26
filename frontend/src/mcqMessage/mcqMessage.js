import React, { useState } from 'react';
import './mcqMessage.css';
import ReactMarkdown from 'react-markdown';

const MCQMessage = ({ question, options, onOptionSelect, correctAnswer, onEvaluationComplete }) => {
    console.log(correctAnswer);
    const [selectedOption, setSelectedOption] = useState(null);
    const [evaluation, setEvaluation] = useState(null);

    const handleOptionSelect = (optionKey) => {
        if (selectedOption) return;
        setSelectedOption(optionKey);

        // // Send the selected option to the backend for evaluation
        // fetch('http://127.0.0.1:5000/api/evaluate_answer', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({ question: question, selected_answer: options[optionKey].value })
        // })
        // .then(response => response.json())
        // .then(data => {
        //     setEvaluation(options[optionKey].explanation);
        // })
        // .catch(error => {
        //     console.error('Error:', error);
        // });
        if(options[optionKey].isCorrectOption)  {
            setEvaluation("Yayy!! Your answer is correct.\n Below is the explanation for it. \n\n" + options[optionKey].explanation);
        }
        else{
            setEvaluation("I am afraid your answer is wrong!!. The right answer is: "+ correctAnswer)
        }
        onEvaluationComplete();
        onOptionSelect(optionKey);
    };

    return (
        <div className="mcq-message">
            <p className="question">{question}</p>
            <ul className="options">
                {Object.entries(options).map(([key, option]) => (
                    <li
                        key={key}
                        className={`option ${selectedOption === key ? 'selected' : ''}`}
                        onClick={() => handleOptionSelect(key)}
                    >
                        {key}: {option.value}
                    </li>
                ))}
            </ul>
            {evaluation && (
                <div className="evaluation">
                    <ReactMarkdown>{evaluation}</ReactMarkdown>
                </div>
            )}
        </div>
    );
};

export default MCQMessage;
