import streamlit as st
import os
from openai import OpenAI
from scripts.utils import construct_prompt

def build_additional_information():
    patient_dict = {
        "gender": st.session_state.get('gender') if st.session_state.get('gender') not in (None, '') else 'Unknown',
        "age": f"{st.session_state['age']} year old" if st.session_state.get('age') not in (None, '') else 'Unknown',
        "location": st.session_state.get('location') if st.session_state.get('location') not in (None, '') else 'Unknown',
        "travel_history": st.session_state.get('travel_history') if st.session_state.get('travel_history') not in (None, '') else 'Unknown'
    }

    additional_information = (
        f"Gender: {patient_dict['gender']}\n"
        f"Age: {patient_dict['age']}\n"
        f"Location: {patient_dict['location']}\n"
        f"Recent travel places: {patient_dict['travel_history']}\n"
    )
    
    return additional_information

def run_conversation_mode():
    st.title('Conversation-mode 💬')

    st.subheader('Instructions :')

    # add some text under the title, to give more context and description about the chatbot use
    st.write("""
            <div style="padding: 10px;">
                Provide <b>detailed</b> information about the patient's condition, including: 
                <ul>
                    <li><span font-weight:bold; padding:2px;">Symptoms</span></li>
                    <li><span font-weight:bold; padding:2px;">Pain</span></li>
                    <li><span font-weight:bold; padding:2px;">Medical history</span></li>
                    <li><span font-weight:bold; padding:2px;">Test results</span></li> 
                    <li><span font-weight:bold; padding:2px;">Relevant context</span></li> 
                </ul>
                This will help the model act as a medical assistant for diagnostic and treatment advice.
            </div>
            """, unsafe_allow_html=True)
    
    # Patient information inputs
    st.subheader('Patient Information :')
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox('Gender', ('Male', 'Female', 'Other'), key='gender')
        location = st.text_input('Location/Region', key='location')
        # infant = st.checkbox('Infant', key='infant')
    
    with col2:
        age = st.number_input('Age', min_value=0, max_value=120, key='age')
        travel_history = st.text_input('Recent travel places', key='travel_history')
        

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

        # default values
        temperature = 0.6
        top_p = 0.9
        max_tokens = 1024

        response = client.chat.completions.create(model="llama-2-70b-meditron", messages=prompt_input, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        return response.choices[0].message.content

    def generate_response(prompt_input):
        # system_prompt_path = os.path.join('prompts', 'system_prompt_conversation.txt')
        # with open(system_prompt_path, 'r') as file:
        #     system_prompt_content = file.read().strip()
        # system_prompt_content = system_prompt_content.replace("ADDITIONAL_INFORMATION", build_additional_information())
        # print(system_prompt_content)

        system_prompt_content = construct_prompt()
        system_prompt_content = system_prompt_content.replace("ADDITIONAL_INFORMATION", build_additional_information())

        print("SYSTEM PROMPT ::: ", system_prompt_content)

        if len(st.session_state.conversation_messages) != 0:
            system_prompt_content = system_prompt_content + "Here is the conversation so far: \n"
            
        prompt = [{"role": "system", "content": system_prompt_content}] + st.session_state.conversation_messages
        
        # print("PROMPT ::: ", prompt)
        
        output = llm_generate_response(prompt)
        return output

    # User-provided prompt
    if prompt := st.chat_input("How can I assist you today ?"):
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