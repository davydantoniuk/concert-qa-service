from utils.llama_client import classify_text

def is_relevant_concert_text(text: str) -> bool:
    prompt = (
        "Is the following document about a concert tour or related details such as venues, artists, dates, "
        "logistics, or performances planned for 2025-2026? Answer with 'yes' or 'no'.\n\n"
        f"{text[:3000]}"  # Limit length to 3000 characters for the model for efficiency
    )
    result = classify_text(prompt)
    return "yes" in result.lower()