import os
from typing import Tuple

from ingestion.keyword_filter import is_relevant_concert_text
from utils.llama_client import summarize_text
from utils.text_cleaner import extract_text_from_file
from vector_store.store_manager import embed_and_store

def handle_ingestion(input_text: str = None, file_path: str = None) -> Tuple[bool, str]:
    # Extract raw text
    if file_path:
        raw_text = extract_text_from_file(file_path)
    elif input_text:
        raw_text = input_text.strip()
    else:
        return False, "No input provided."

    if not raw_text:
        return False, "Could not extract any text."

    # Relevance check 
    if not is_relevant_concert_text(raw_text):
        return False, "This content doesn't seem to be about concert tours."

    # Optional summary for user confirmation
    summary = summarize_text(raw_text)

    # Embed and store full document 
    embed_and_store(raw_text, metadata={"source": file_path or "user input"})

    # Return to user
    return True, f"Document ingested successfully!\n\nSummary:\n{summary}"