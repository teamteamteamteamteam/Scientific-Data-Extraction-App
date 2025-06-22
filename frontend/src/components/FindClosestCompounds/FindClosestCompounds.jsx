import './FindClosestCompounds.css';
import React, { useState } from 'react';
const FindClosestCompounds = ({ onClick }) => {
    const [inputValue, setInputValue] = useState("");

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue !== '') {
            onClick(Number(inputValue));
        }
    };

    return (
        <div className="find-closest-compounds">
            <h1 className="title">Find Closest Compounds</h1>
            <form className="input-container" onSubmit={handleSubmit}>
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
                    type="submit"
                >
                    FIND
                </button>
            </form>
        </div>
    );
};

export default FindClosestCompounds;