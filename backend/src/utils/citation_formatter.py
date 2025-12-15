from typing import List, Dict, Any
from src.models.query_result import SourceCitation


def format_citations_for_frontend(citations: List[SourceCitation]) -> List[Dict[str, Any]]:
    """
    Format citations for frontend display with proper structure.

    Args:
        citations: List of SourceCitation objects

    Returns:
        List of dictionaries formatted for frontend consumption
    """
    formatted_citations = []
    for citation in citations:
        formatted_citations.append({
            "url": citation.url,
            "title": citation.title,
            "relevance_score": citation.relevance_score,
            "display_text": f"{citation.title} (Relevance: {citation.relevance_score:.2f})"
        })
    return formatted_citations


def create_citation_links(citations: List[SourceCitation], base_url: str = "") -> List[Dict[str, Any]]:
    """
    Create citation links with proper formatting for the frontend.

    Args:
        citations: List of SourceCitation objects
        base_url: Base URL to prepend to relative URLs

    Returns:
        List of dictionaries with properly formatted citation links
    """
    citation_links = []
    for citation in citations:
        # Ensure the URL is properly formatted
        url = citation.url
        if base_url and not url.startswith(('http://', 'https://')):
            url = base_url + url if url.startswith('/') else f"{base_url}/{url}"

        citation_links.append({
            "url": url,
            "title": citation.title,
            "relevance_score": citation.relevance_score,
            "link_text": f"View source ({citation.title})",
            "is_external": url.startswith(('http://', 'https://'))
        })

    return citation_links


def sort_citations_by_relevance(citations: List[SourceCitation]) -> List[SourceCitation]:
    """
    Sort citations by relevance score in descending order.

    Args:
        citations: List of SourceCitation objects

    Returns:
        List of SourceCitation objects sorted by relevance score
    """
    return sorted(citations, key=lambda x: x.relevance_score, reverse=True)


def filter_citations_by_threshold(citations: List[SourceCitation], min_score: float = 0.5) -> List[SourceCitation]:
    """
    Filter citations to only include those above a certain relevance threshold.

    Args:
        citations: List of SourceCitation objects
        min_score: Minimum relevance score threshold

    Returns:
        List of SourceCitation objects with scores above the threshold
    """
    return [citation for citation in citations if citation.relevance_score >= min_score]


def generate_citation_summary(citations: List[SourceCitation]) -> Dict[str, Any]:
    """
    Generate a summary of the citations including statistics.

    Args:
        citations: List of SourceCitation objects

    Returns:
        Dictionary with citation summary statistics
    """
    if not citations:
        return {
            "total_citations": 0,
            "average_relevance": 0.0,
            "highest_relevance": 0.0,
            "lowest_relevance": 0.0
        }

    scores = [citation.relevance_score for citation in citations]
    return {
        "total_citations": len(citations),
        "average_relevance": sum(scores) / len(scores),
        "highest_relevance": max(scores),
        "lowest_relevance": min(scores),
        "citations_above_075": len([s for s in scores if s >= 0.75]),
        "citations_above_05": len([s for s in scores if s >= 0.5])
    }