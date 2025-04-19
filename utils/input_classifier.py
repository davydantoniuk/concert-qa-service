import re

def is_event_description(text: str) -> bool:
    if not text:
        return False  # empty or None input can't be event info

    # Rudimentary keyword-based scoring
    keywords = ["concert", "tour", "venue", "date", "perform", "tickets", "stage", "logistics"]
    score = sum(1 for k in keywords if k in text.lower())

    # Simple question check
    is_question = text.strip().endswith("?") or text.lower().startswith(("who", "where", "what", "is", "are", "will", "when"))

    return score >= 2 and not is_question

def is_relevant_question(text: str) -> bool:
    """
    Determine if the user question is related to concert tours.
    """
    concert_keywords = ["concert", "tour", "perform", "venue", "show", "tickets", "artist", "band"]
    text = text.lower()

    match_count = sum(1 for kw in concert_keywords if kw in text)
    return match_count >= 1  # Tune this threshold as needed
