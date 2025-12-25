from typing import Union


def validate_text_length(text: str, max_words: int = 1000) -> bool:
    """
    Validate that text does not exceed the maximum word count.

    Args:
        text: The text to validate
        max_words: Maximum number of words allowed (default 1000)

    Returns:
        True if text is within limit, False otherwise
    """
    if not text:
        return True  # Empty text is valid

    word_count = len(text.split())
    return word_count <= max_words


def get_word_count(text: str) -> int:
    """
    Get the word count of a text.

    Args:
        text: The text to count words in

    Returns:
        Number of words in the text
    """
    if not text:
        return 0

    return len(text.split())


def validate_text_content(text: str, min_length: int = 1, max_length: int = 5000) -> tuple[bool, str]:
    """
    Validate text content for basic requirements.

    Args:
        text: The text to validate
        min_length: Minimum character length
        max_length: Maximum character length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(text) < min_length:
        return False, f"Text is too short. Minimum {min_length} characters required."

    if len(text) > max_length:
        return False, f"Text is too long. Maximum {max_length} characters allowed."

    # Additional checks can be added here
    # For example, checking for valid characters, etc.

    return True, ""


def validate_selected_text_for_context(selected_text: str) -> tuple[bool, str]:
    """
    Validate selected text specifically for use in the selected text context mode.

    Args:
        selected_text: The text that was selected by the user

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if text is provided
    if not selected_text or not selected_text.strip():
        return False, "Selected text cannot be empty."

    # Check length (in words)
    word_count = get_word_count(selected_text)
    if word_count > 1000:
        return False, f"Selected text is too long ({word_count} words). Maximum 1000 words allowed."

    if word_count < 5:  # At least 5 words for meaningful context
        return False, f"Selected text is too short ({word_count} words). Minimum 5 words required for context."

    # Check character length
    if len(selected_text) > 5000:  # Roughly 5000 characters max
        return False, "Selected text exceeds maximum character length."

    return True, ""


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing potentially harmful content.

    Args:
        text: The text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return text

    # Remove excessive whitespace
    sanitized = ' '.join(text.split())

    # Additional sanitization can be added here if needed
    # For example, removing potentially malicious content

    return sanitized