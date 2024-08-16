import streamlit as st
import os
from openai import OpenAI
from scripts.utils import construct_prompt

def run_conversation_general_mode():
    st.title('Conversation-General 💬')

    st.subheader('Instructions :')

    st.write("""
            <div style="padding: 10px;">
                You can ask the chatbot any general questions about medical guidelines or practices and have a conversation with it.
                The chatbot will provide you with the most accurate and relevant information based on the context of the conversation.
                If you want to discuss a patient's condition, please switch to the <b>Conversation-patient</b> mode.
            </div>
            """, unsafe_allow_html=True)

    if "conversation_general_messages" not in st.session_state:
        st.session_state.conversation_general_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.conversation_general_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # def clear_chat_history():
    #     st.session_state.conversation_general_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    # st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def llm_generate_response(prompt_input):
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")

        # default values
        temperature = 0.6
        top_p = 0.9
        max_tokens = 1024

        response = client.chat.completions.create(model="llama-3-70b-meditron", messages=prompt_input, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        return response.choices[0].message.content

    def generate_response(prompt_input):

        system_prompt_content = construct_prompt("general")

        print("SYSTEM PROMPT ::: ", system_prompt_content)

        if len(st.session_state.conversation_general_messages) != 0:
            system_prompt_content = system_prompt_content + "Here is the conversation so far: \n"
            
        prompt = [{"role": "system", "content": system_prompt_content}] + st.session_state.conversation_general_messages + [{"role": "user", "content": prompt_input}]
                
        output = llm_generate_response(prompt)
        return output

    # User-provided prompt
    if prompt := st.chat_input("How can I assist you today ?"):
        st.session_state.conversation_general_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.conversation_general_messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                placeholder = st.empty()
                full_response = response
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.conversation_general_messages.append(message)