import streamlit as st
from openai import OpenAI
import os

def run_conversation_mode():
    st.title('Conversation-mode')

    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.8, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_tokens = st.sidebar.slider('max_tokens', min_value=32, max_value=512, value=256, step=8)

    if "conversation_messages" not in st.session_state:
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.conversation_messages:
        with st.chat_message(message["role"]):
            #st.markdown(f"<div class='chat-{message['role']}'>{message['content']}</div>", unsafe_allow_html=True)
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def llm_generate_response(prompt_input):
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")
        response = client.chat.completions.create(model="llama-2-70b-meditron", messages=prompt_input, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
        return response.choices[0].message.content

    def generate_response(prompt_input):
        # Define the path to the system prompt file
        system_prompt_path = os.path.join('prompts', 'system_prompt_conversation.txt')
        
        # Read the system prompt from the file
        with open(system_prompt_path, 'r') as file:
            system_prompt_content = file.read().strip()

        # print(system_prompt_content)

        prompt = [{"role": "system", "content": system_prompt_content}] + st.session_state.conversation_messages + [{"role": "user", "content": prompt_input}]
        output = llm_generate_response(prompt)
        return output

    # User-provided prompt
    if prompt := st.chat_input("How can I help you ?"):
        st.session_state.conversation_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.conversation_messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                placeholder = st.empty()
                full_response = response
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.conversation_messages.append(message)
