from qa.rag_pipeline import query_rag_system
from search.ddg_search import perform_search
from utils.llama_client import summarize_text
from utils.input_classifier import is_relevant_question

def route_query(user_input: str, chat_history: list = None) -> str:
    if not is_relevant_question(user_input):
        return (
            ":red[❌ This question doesn’t seem to be about concert tours.]\n\n"
            "Please ask about 2025–2026 concerts, venues, artists, or related information."
        )

    # Try internal RAG system
    rag_answer = query_rag_system(user_input, chat_history=chat_history)

    if rag_answer and "no information" not in rag_answer.lower():
        return f"🧠 Based on internal documents:\n\n{rag_answer}"

    # If RAG fails — fallback to web
    fallback_message = "🧠 No relevant info found in internal documents.\n\n🔍 Searching the web..."
    print(fallback_message)

    web_data = perform_search(user_input)

    if web_data:
        # Add chat history to prompt (last 4 messages)
        history = format_chat_history(chat_history)
        prompt = (
            f"Conversation so far:\n{history}\n\n"
            f"Now use the public info below to answer the question:\n\n"
            f"{web_data}\n\n"
            f"Question: {user_input}"
        )
        web_answer = summarize_text(prompt)
        return f"{fallback_message}\n\n🌐 Based on live web search:\n\n{web_answer}"

    return (
        f"{fallback_message}\n\n"
        "❌ I couldn't find any useful info about that concert even on the web."
    )

def format_chat_history(chat_history):
    if not chat_history:
        return ""
    last_msgs = chat_history[-4:]  # last 4 turns
    return "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in last_msgs])