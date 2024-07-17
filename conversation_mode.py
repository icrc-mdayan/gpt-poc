import streamlit as st
import os
from openai import OpenAI

def build_additional_information():
    gender = st.session_state.get('gender') if st.session_state.get('gender') else 'Not specified'
    age = str(st.session_state.get('age')) + " year old" if st.session_state.get('age') else 'Not specified'
    location = st.session_state.get('location') if st.session_state.get('location') else 'Not specified'
    travel_history = st.session_state.get('travel_history') if st.session_state.get('travel_history') else 'Not specified'
    
    additional_information = f"Gender: {gender}\nAge: {age}\nLocation: {location}\nRecent travel places: {travel_history}\n"
    if st.session_state.get('infant', False):
        additional_information += "Infant: Yes\n"
    
    return additional_information

def run_conversation_mode():
    st.title('Conversation-mode 💬')

    # add some text under the title, to give more context and description about the chatbot use
    st.write("""
             You are expected to give information about a patient's condition to the model, that will act as a medical assistant trying to understand the case and to provide diagnostic and treatment advice. \n
             Please be as detailed as possible, mentioning the symptoms, the patient's medical history, and any other relevant information such as the pain, additional medical tests and contextual factors.
             """)
    
    # Patient information inputs
    st.subheader('Patient Information')
    gender = st.selectbox('Gender', ('Male', 'Female', 'Other'), key='gender')
    age = st.number_input('Age', min_value=0, max_value=120, key='age')
    location = st.text_input('Location', key='location')
    travel_history = st.text_input('Recent travel places', key='travel_history')
    infant = st.checkbox('Infant', key='infant')

    # temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.8, step=0.01)
    # top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_tokens = st.sidebar.slider('max_tokens', min_value=32, max_value=512, value=256, step=8)

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

        # default values
        temperature = 0.8
        top_p = 0.9
        max_tokens = 256

        response = client.chat.completions.create(model="llama-3-70b-meditron", messages=prompt_input, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
        return response.choices[0].message.content

    def generate_response(prompt_input):
        # Define the path to the system prompt file
        system_prompt_path = os.path.join('prompts', 'system_prompt_conversation.txt')
        
        # Read the system prompt from the file
        with open(system_prompt_path, 'r') as file:
            system_prompt_content = file.read().strip()

        # additional_information = f"Gender: {st.session_state.get('gender', 'Not specified')}\nAge: {st.session_state.get('age', 'Not specified')} yearl old\nLocation: {st.session_state.get('location', 'Not specified')}\nRecent travel places: {st.session_state.get('travel_history', 'Not specified')}\n"
        # if st.session_state.get('infant', False):
        #     additional_information += "Infant: Yes\n"
        
        system_prompt_content = system_prompt_content.replace("ADDITIONAL_INFORMATION", build_additional_information())
        
        print(system_prompt_content)

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
