import streamlit as st
from utils.input_classifier import is_event_description
from ingestion.ingestion_handler import handle_ingestion
from main_router import route_query

# ----------------- Streamlit Config -----------------
st.set_page_config(page_title="🎤 Concert Tour Chatbot", layout="centered")
st.title("Concert Tour Assistant")
st.markdown("Ask about 2025–2026 concert tours or paste full event details.")

# ----------------- Chat State Init -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------- Clear Chat Logic -----------------
def clear_chat():
    st.session_state.messages = []
    st.session_state.clear_flag = True  # trigger flag

# Display button and handle
if st.button("🧹 Clear Chat History"):
    clear_chat()

# Use flag to control rerun behavior
if st.session_state.get("clear_flag", False):
    st.session_state.clear_flag = False  # reset flag
    st.rerun()

# ----------------- Chat Interface -----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------- User Input Box -----------------
user_input = st.chat_input("Ask a question or paste concert details...")

if user_input and user_input.strip():
    # Add user message to history immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Process input (auto-route: ingestion vs question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if is_event_description(user_input):
                success, response = handle_ingestion(input_text=user_input)

                if success:
                    st.success("✅ Document ingested successfully!")
                    st.markdown(f"📝 Summary:\n\n{response}")
                    assistant_message = f"✅ Document saved.\n\n**Summary:**\n{response}"
                else:
                    st.warning(response)
                    assistant_message = response
            else:
                answer = route_query(user_input, chat_history=st.session_state.messages)
                st.markdown(answer)
                assistant_message = answer

    # Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})