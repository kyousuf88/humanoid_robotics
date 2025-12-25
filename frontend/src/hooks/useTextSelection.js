import { useState, useEffect } from 'react';

const useTextSelection = () => {
  const [selectedText, setSelectedText] = useState('');
  const [isSelecting, setIsSelecting] = useState(false);

  // Function to get currently selected text
  const getSelectedText = () => {
    return window.getSelection ? window.getSelection().toString().trim() : '';
  };

  // Function to handle text selection
  const handleTextSelection = () => {
    const text = getSelectedText();

    if (text) {
      // Check if selection is too long (more than 1000 words)
      const wordCount = text.split(/\s+/).length;
      if (wordCount > 1000) {
        alert(`Selected text is too long (${wordCount} words). Please select fewer than 1000 words.`);
        return null;
      }

      setSelectedText(text);
      return text;
    }

    return null;
  };

  // Function to start selection mode
  const startSelection = () => {
    setIsSelecting(true);
    // Clear any existing selection
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    }
  };

  // Function to clear selection
  const clearSelection = () => {
    setSelectedText('');
    setIsSelecting(false);
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    }
  };

  // Function to validate text selection
  const validateSelection = (text) => {
    if (!text) {
      return { valid: false, message: 'No text selected' };
    }

    const wordCount = text.split(/\s+/).length;
    if (wordCount > 1000) {
      return { valid: false, message: `Selected text is too long (${wordCount} words). Maximum 1000 words allowed.` };
    }

    if (wordCount < 5) {
      return { valid: false, message: `Selected text is too short (${wordCount} words). Minimum 5 words required.` };
    }

    return { valid: true, message: '' };
  };

  // Add event listener for mouse up to detect text selection
  useEffect(() => {
    if (!isSelecting) return;

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
  }, [isSelecting]);

  return {
    selectedText,
    setSelectedText,
    isSelecting,
    startSelection,
    clearSelection,
    getSelectedText,
    handleTextSelection,
    validateSelection
  };
};

export default useTextSelection;