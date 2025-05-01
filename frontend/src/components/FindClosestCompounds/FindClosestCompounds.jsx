import './FindClosestCompounds.css';
import React, { useState } from 'react';
const FindClosestCompounds = ({ onClick }) => {
    const [inputValue, setInputValue] = useState(null);

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    return (
        <div className="find-closest-compounds">
            <h1 className="title">Find Closest Compounds</h1>
            <div className="input-container">
                <input
                    className="input-field"
                    type="number"
                    min="0"
                    placeholder="Enter a number"
                    value={inputValue}
                    onChange={handleInputChange}
                />
                <button
                    className="find-button"
                    onClick={() => onClick(Number(inputValue))}
                >
                    FIND
                </button>
            </div>
        </div>
    );
};

export default FindClosestCompounds;