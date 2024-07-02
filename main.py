import streamlit as st
from rag_mode import run_rag_mode
from conversation_mode import run_conversation_mode

# App title
st.set_page_config(page_title="🦙💬 random Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 random Chatbot')

    st.subheader('Models and parameters')
    selected_mode = st.selectbox('Choose a mode', ['Conversation-mode', 'RAG-mode'], key='selected_mode')

# Load the appropriate mode
if selected_mode == 'Conversation-mode':
    run_conversation_mode()
else:
    run_rag_mode()