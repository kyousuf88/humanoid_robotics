import React from 'react';
import PropTypes from 'prop-types';

const CitationDisplay = ({ citations, onClickCitation }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div className="citation-display">
      <h4>Source Citations:</h4>
      <ul className="citations-list">
        {citations.map((citation, index) => (
          <li key={index} className="citation-item">
            <a
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              className="citation-link"
              onClick={(e) => onClickCitation && onClickCitation(citation, e)}
            >
              {citation.title}
            </a>
            <span className="relevance-score" title={`Relevance: ${citation.relevance_score}`}>
              ({(citation.relevance_score * 100).toFixed(1)}%)
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

CitationDisplay.propTypes = {
  citations: PropTypes.arrayOf(
    PropTypes.shape({
      url: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      relevance_score: PropTypes.number.isRequired
    })
  ),
  onClickCitation: PropTypes.func
};

export default CitationDisplay;