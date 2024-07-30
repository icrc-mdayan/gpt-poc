import streamlit as st
from rag_mode import run_rag_mode
from conversation_patient_mode import run_conversation_patient_mode, build_additional_information
from conversation_general_mode import run_conversation_general_mode
import os
from datetime import datetime
import nltk
from nltk.data import find

def download_nltk_resources():
    try:
        # Check if the 'punkt' resource is already available
        find('tokenizers/punkt')
    except LookupError:
        # If not found, download the resource
        nltk.download('punkt')
download_nltk_resources()
# App title
st.set_page_config(page_title="🧑‍⚕️💬 Meditron-3-70B 🩺")

# Function to save conversation to a txt file with Markdown formatting
def save_conversation(conversation, mode, additional_patient_info=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_md = f"logs/md/{mode}_{timestamp}.md"
    with open(filename_md, "w") as file:
        file.write(f"# Conversation Log ({mode})\n\n")
        file.write(f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if additional_patient_info:
            file.write(f"**Patient Information**:\n")
            file.write(f"{additional_patient_info}\n\n")
        for message in conversation:
            role = message["role"].capitalize()
            content = message["content"]
            if role == "Assistant":
                file.write(f"### {role}:\n\n")
                file.write(f'<div style="background-color: #B7E6F3; padding: 10px; border-radius: 5px;">\n')
                file.write(f"{content}\n")
                file.write(f"</div>\n\n")
            elif role == "User":
                file.write(f"### {role}:\n\n")
                file.write(f'<div style="background-color: #F4DDA8; padding: 10px; border-radius: 5px;">\n')
                file.write(f"{content}\n")
                file.write(f"</div>\n\n")
        file.close()

    filename_txt = f"logs/txt/{mode}_{timestamp}.txt"
    with open(filename_txt, "w") as file:
        file.write(f"Conversation Log ({mode})\n\n")
        file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if additional_patient_info:
            file.write(f"Patient Information:\n\n")
            file.write(f"{additional_patient_info}\n\n")
        for message in conversation:
            role = message["role"].capitalize()
            content = message["content"]
            file.write(f"{role}:\n")
            file.write(f" - {content}\n")
        file.close()
        
    st.sidebar.success(f"Conversation saved to {filename_md} and {filename_txt}")

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Replicate Credentials
with st.sidebar:
    st.title("🧑‍⚕️💬 Meditron-3-70B 🩺")

    st.subheader('Mode Selection')
    selected_mode = st.radio('Choose a mode', ['ICRC-knowledge based chatbot', 'Conversation-patient', 'Conversation-general'], key='selected_mode')

    st.subheader('Save and clear chat history')

    # Add a button to save the conversation
    if st.sidebar.button("Save Conversation"):
        if selected_mode == 'ICRC-knowledge based chatbot' and "rag_messages" in st.session_state:
            save_conversation(st.session_state.rag_messages, selected_mode)
        elif selected_mode == 'Conversation-patient' and "conversation_messages" in st.session_state:
            save_conversation(st.session_state.conversation_messages, selected_mode, build_additional_information())
        elif selected_mode == 'Conversation-general' and "conversation_general_messages" in st.session_state:
            save_conversation(st.session_state.conversation_general_messages, selected_mode)

# Load the appropriate mode
if selected_mode == 'ICRC-knowledge based chatbot':
    run_rag_mode()
elif selected_mode == 'Conversation-patient':
    run_conversation_patient_mode()
else:
    run_conversation_general_mode()