import ollama

DEFAULT_MODEL = "llama3.1:latest"

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following concert-related document:\n\n{text[:3000]}"
    response = ollama.chat(model=DEFAULT_MODEL, messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content'].strip()

def classify_text(text: str) -> str:
    prompt = (
        "Is the following text about a concert tour or related topics like performances, venues, or logistics? "
        "Please answer with only 'Yes' or 'No'.\n\n"
        f"{text[:3000]}"
    )
    response = ollama.chat(model=DEFAULT_MODEL, messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content'].strip()
