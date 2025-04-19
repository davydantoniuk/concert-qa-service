from vector_store.store_manager import search_similar
from utils.llama_client import summarize_text

def query_rag_system(query: str, chat_history: list = None) -> str:
    relevant_docs = search_similar(query)

    if not relevant_docs:
        return None

    context = "\n\n".join([doc["text"] for doc in relevant_docs])
    history = format_chat_history(chat_history)

    prompt = (
        f"Conversation so far:\n{history}\n\n"
        f"Based on the following concert tour information, answer the question below.\n\n"
        f"{context}\n\n"
        f"Question: {query}"
    )

    return summarize_text(prompt)

def format_chat_history(chat_history):
    if not chat_history:
        return ""
    last_msgs = chat_history[-4:]
    return "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in last_msgs])