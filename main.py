import streamlit as st
from rag_mode import run_rag_mode
from conversation_mode import run_conversation_mode
import os
from datetime import datetime

# App title
st.set_page_config(page_title="🧑‍⚕️💬 Meditron-3-70B 🩺")

# Function to save conversation to a txt file with Markdown formatting
def save_conversation(conversation, mode):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/{mode}_{timestamp}.md"
    with open(filename, "w") as file:
        file.write(f"# Conversation Log ({mode})\n\n")
        file.write(f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for message in conversation:
            role = message["role"].capitalize()
            content = message["content"]
            file.write(f"### {role}:\n\n")
            file.write(f"> {content}\n\n")
    st.sidebar.success(f"Conversation saved to {filename}")


# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Replicate Credentials
with st.sidebar:
    st.title("🧑‍⚕️💬 Meditron-3-70B 🩺")

    st.subheader('Models and parameters')
    selected_mode = st.selectbox('Choose a mode', ['RAG-mode', 'Conversation-mode'], key='selected_mode')

    # Add a button to save the conversation
    if st.sidebar.button("Save Conversation"):
        if selected_mode == 'RAG-mode' and "rag_messages" in st.session_state:
            save_conversation(st.session_state.rag_messages, "RAG-mode")
        elif selected_mode == 'Conversation-mode' and "conversation_messages" in st.session_state:
            save_conversation(st.session_state.conversation_messages, "Conversation-mode")

# Load the appropriate mode
if selected_mode == 'RAG-mode':
    run_rag_mode()
else:
    run_conversation_mode()
