import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const TextSelector = ({ onSelectText, selectedText }) => {
  const [isSelecting, setIsSelecting] = useState(false);
  const [currentSelection, setCurrentSelection] = useState('');

  // Function to handle text selection
  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();

    if (selectedText) {
      // Check if selection is too long (more than 1000 words)
      const wordCount = selectedText.split(/\s+/).length;
      if (wordCount > 1000) {
        alert(`Selected text is too long (${wordCount} words). Please select fewer than 1000 words.`);
        return;
      }

      setCurrentSelection(selectedText);
      onSelectText(selectedText);
    }
  };

  // Add event listener for mouse up to detect text selection
  useEffect(() => {
    const handleMouseUp = () => {
      if (isSelecting) {
        handleTextSelection();
        setIsSelecting(false);
      }
    };

    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isSelecting, onSelectText]);

  const startSelection = () => {
    setIsSelecting(true);
    // Clear any existing selection
    window.getSelection().removeAllRanges();
  };

  const clearSelection = () => {
    onSelectText('');
    setCurrentSelection('');
    window.getSelection().removeAllRanges();
  };

  return (
    <div className="text-selector">
      <div className="selection-controls">
        <button
          className={`select-btn ${isSelecting ? 'active' : ''}`}
          onClick={startSelection}
          title="Start text selection mode"
        >
          {isSelecting ? 'Selecting...' : 'Select Text'}
        </button>

        {selectedText && (
          <button
            className="clear-btn"
            onClick={clearSelection}
            title="Clear selected text"
          >
            Clear Selection
          </button>
        )}
      </div>

      {selectedText && (
        <div className="selected-text-preview">
          <div className="preview-header">
            <strong>Selected Text ({selectedText.split(/\s+/).length} words):</strong>
            <span
              className="preview-toggle"
              onClick={() => document.querySelector('.selected-text-content').classList.toggle('collapsed')}
            >
              {document.querySelector('.selected-text-content')?.classList.contains('collapsed') ? 'Expand' : 'Collapse'}
            </span>
          </div>
          <div className="selected-text-content">
            {selectedText.substring(0, 200)}{selectedText.length > 200 ? '...' : ''}
          </div>
          {selectedText.length > 200 && (
            <div className="full-text" style={{ display: 'none' }}>
              {selectedText}
            </div>
          )}
        </div>
      )}

      {isSelecting && (
        <div className="selection-instruction">
          Highlight text on the page to select it for questioning.
        </div>
      )}
    </div>
  );
};

TextSelector.propTypes = {
  onSelectText: PropTypes.func.isRequired,
  selectedText: PropTypes.string
};

export default TextSelector;