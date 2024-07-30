import streamlit as st
import os
from openai import OpenAI
from scripts.utils import construct_prompt

def build_additional_information():
    patient_dict = {
        "Sex": st.session_state.get('Sex') if st.session_state.get('Sex') not in (None, '') else None,
        "age": f"{st.session_state['age']} year old" if st.session_state.get('age') not in (None, '') else None,
        "location": st.session_state.get('location') if st.session_state.get('location') not in (None, '') else 'Unknown',
        "travel_history": st.session_state.get('travel_history') if st.session_state.get('travel_history') not in (None, '') else 'Unknown'
    }

    additional_information = (
        f"Sex: {patient_dict['Sex']}\n"
        f"Age: {patient_dict['age']}\n"
        f"Location: {patient_dict['location']}\n"
        f"Recent travel places: {patient_dict['travel_history']}\n"
    )
    
    return additional_information

def run_conversation_patient_mode():
    st.title('Conversation-Patient 💬')

    st.subheader('Instructions :')

    # add some text under the title, to give more context and description about the chatbot use
    st.write("""
            <div style="padding: 10px;">
                This mode is designed to help you to come up with a diagnostic and treatment when discussing a specific patient case.\n You may choose to provide <b>detailed</b> information about the patient's condition, including:
                <ul>
                    <li><span font-weight:bold; padding:2px;">Symptoms</span></li>
                    <li><span font-weight:bold; padding:2px;">Pain</span></li>
                    <li><span font-weight:bold; padding:2px;">Medical history</span></li>
                    <li><span font-weight:bold; padding:2px;">Test results</span></li> 
                    <li><span font-weight:bold; padding:2px;">Relevant context</span></li> 
                </ul>
                This optional information can help the model act as a medical assistant for diagnostic and treatment advice.
            </div>
            """, unsafe_allow_html=True)

    
    # Patient information inputs
    st.subheader('Patient Information :')
    col1, col2 = st.columns(2)

    # set the patient information using st.session_state['key'] = default value
    # st.session_state['location'] = ''
    # st.session_state['age'] = None
    # st.session_state['Sex'] = None
    # st.session_state['travel_history'] = ''
    
    with col1:
        Sex = st.selectbox('Sex', ('Male', 'Female', 'Other'), key='Sex')
        location = st.text_input('Location/Region', key='location', placeholder='City, Country', value=None)
        # infant = st.checkbox('Infant', key='infant')
    
    with col2:
        age = st.number_input('Age', min_value=0, max_value=120, key='age', placeholder='-', value=None)
        travel_history = st.text_input('Recent travel places', key='travel_history', placeholder='City, Country', value=None)

    if "conversation_messages" not in st.session_state:
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.conversation_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.session_state['location'] = ''
        st.session_state['age'] = None
        st.session_state['Sex'] = 'Male'
        st.session_state['travel_history'] = ''

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def llm_generate_response(prompt_input):
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")

        # default values
        temperature = 0.6
        top_p = 0.9
        max_tokens = 1024

        response = client.chat.completions.create(model="llama-3-70b-meditron", messages=prompt_input, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        return response.choices[0].message.content

    def generate_response(prompt_input):
        system_prompt_content = construct_prompt("patient")
        system_prompt_content = system_prompt_content.replace("ADDITIONAL_INFORMATION", build_additional_information())

        print("SYSTEM PROMPT ::: ", system_prompt_content)

        if len(st.session_state.conversation_messages) != 0:
            system_prompt_content = system_prompt_content + "Here is the conversation so far: \n"
            
        prompt = [{"role": "system", "content": system_prompt_content}] + st.session_state.conversation_messages + [{"role": "user", "content": prompt_input}]
                
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