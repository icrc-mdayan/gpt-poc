import streamlit as st
from openai import OpenAI


def run_rag_mode():
    # Page title for RAG-mode
    st.title('RAG-mode')

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

    def llm_generate_response(prompt_input):
        url = "http://104.171.203.227:8000/v1/chat/completions"


        client = OpenAI(base_url = "http://104.171.203.227:8000/v1", api_key = "EMPTY")
        response = client.chat.completions.create(model="llama-2-70b-meditron", messages=prompt_input)

        return response.choices[0].message.content                  

    def generate_response(prompt_input):
        system_prompt = "You are a helpful medical assistant."
        if st.session_state.messages is None:
            prompt = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt_input}]
        else:
            prompt = st.session_state.messages
        #prompt.append({"role": "user", "content": prompt_input})
        output = llm_generate_response(prompt)
        return output

    # User-provided prompt
    if prompt := st.chat_input("What bothers you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
