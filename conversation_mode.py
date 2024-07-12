import streamlit as st
from openai import OpenAI
import os

def run_conversation_mode():
    st.title('Conversation-mode')

    if "conversation_messages" not in st.session_state:
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.conversation_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def llm_generate_response(prompt_input):
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")
        response = client.chat.completions.create(model="llama-2-70b-meditron", messages=prompt_input)
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
    if prompt := st.chat_input("What bothers you today?"):
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
