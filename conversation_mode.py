import streamlit as st
from tiny_llama_model import TinyLlamaChat
import random
import time

chat_model = TinyLlamaChat()

def run_conversation_mode():
    # Page title for Conversation-mode
    st.title('Conversation-mode')

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # def generate_response(prompt_input):
    #     string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    #     for dict_message in st.session_state.messages:
    #         if dict_message["role"] == "user":
    #             string_dialogue += "User: " + dict_message["content"] + "\n\n"
    #         else:
    #             string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    #     output = random.choice([
    #                                 "This is a great question, I think I can help you with that. Let me think about it for a moment.",
    #                                 "I'm not sure about that, but I can try to help you. Let me think about it for a moment.",
    #                                 "I will do my best to help you with that. Let me think about it for a moment.",
    #                                 "I am not an LLM model, but I can try to help you. Let me think about it for a moment.",
    #                                 "Hellooo! I am here to help you. Let me think about it for a moment.",
    #     ])
    #     for word in output.split():
    #         yield word + " "
    #         time.sleep(0.05)

    # User-provided prompt
    if prompt := st.chat_input("What bothers you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            response = chat_model.generate_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            # placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
