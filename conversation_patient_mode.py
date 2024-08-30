import streamlit as st
import os
from openai import OpenAI
from scripts.utils import construct_prompt
from fuzzywuzzy import process
from llamaapi import LlamaAPI
from country_cards_utils import *

def build_additional_information():
    patient_dict = {
        "Sex": st.session_state.get('Sex_widget') if st.session_state.get('Sex_widget') not in (None, '') else None,
        "age": f"{st.session_state.get('age_widget')} year old" if st.session_state.get('age_widget') not in (None, '') else None,
        "location": st.session_state.get('location_widget') if st.session_state.get('location_widget') not in (None, '') else 'Unknown',
        "travel_history": st.session_state.get('travel_history_widget') if st.session_state.get('travel_history_widget') not in (None, '') else 'Unknown'
    }

    additional_information = (
        f"Sex: {patient_dict['Sex']}\n"
        f"Age: {patient_dict['age']}\n"
        f"Location: {patient_dict['location']}\n"
        f"Recent travel places: {patient_dict['travel_history']}\n"
    )

    location = st.session_state.get('location_widget')
    sex = st.session_state.get('Sex_widget')
    age = st.session_state.get('age_widget')

    processed_age, processed_sex, processed_location = process_user_entries(age, sex, location)
    additional_information += f"\n" + process_csv(filter_csv(processed_age, processed_sex, processed_location))

    return additional_information

def match_location_country(location):
    country_files = os.listdir("scripts/country_cards/cards_5000")
    fuzzy_match = process.extractOne(location, country_files)
    with open(f"scripts/country_cards/cards_5000/{fuzzy_match[0]}", "r", encoding="utf-8") as file:
        content = file.read()
        return content
    
def run_conversation_patient_mode():

    if "total_text_conversation" not in st.session_state:
        st.session_state.total_text_conversation = ""

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
    
    with col1:
        Sex = st.selectbox('Sex', ('Male', 'Female', 'Other'), key='Sex_widget')
        location = st.text_input('Location/Region', key='location_widget', placeholder='City, Country', value=None)

    with col2:
        age = st.number_input('Age', min_value=0, max_value=120, key='age_widget', placeholder='-', value=None)
        travel_history = st.text_input('Recent travel places', key='travel_history_widget', placeholder='City, Country', value=None)

    if "Sex" not in st.session_state:
        st.session_state.Sex = st.session_state.Sex_widget

    if "location" not in st.session_state:
        st.session_state.location = st.session_state.location_widget

    if "age" not in st.session_state:
        st.session_state.age = st.session_state.age_widget

    if "travel_history" not in st.session_state:
        st.session_state.travel_history = st.session_state.travel_history_widget



    if "conversation_messages" not in st.session_state:
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.conversation_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def llm_generate_response(prompt_input, total_text_conversation):
        # MEDITRON-3 API MANAGEMENT ----------------------------
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")

        temperature = 0.6
        top_p = 0.9
        max_tokens = 1024

        # Add the user's input to the total conversation
        total_text_conversation += f"User: {prompt_input[-1]['content']}\n"

        response = client.chat.completions.create(
            model="llama-3-70b-meditron", 
            messages=prompt_input, 
            temperature=temperature, 
            top_p=top_p,
            max_tokens=max_tokens
        )

        # Add the assistant's response to the total conversation
        total_text_conversation += f"Assistant: {response.choices[0].message.content}\n"

        return response.choices[0].message.content, total_text_conversation
    
        # LLAMA 3.1 API MANAGEMENT ----------------------------
        # llama = LlamaAPI("LA-488cd8bbb61342669fc4c6ce6feb11822f997ac0200f4c12b808766991306fcf")

        # # Add the user's input to the total conversation
        # total_text_conversation += f"User: {prompt_input[-1]['content']}\n"

        # api_request_json = {
        #     "messages": prompt_input,
        #     "stream": False,
        #     "temperature": 0.6,
        #     "max_tokens": 1024,
        #     "top_p": 0.9
        # }

        # response = llama.run(api_request_json)
        # assistant_message = response.json()["choices"][0]["message"]["content"]

        # # Add the assistant's response to the total conversation
        # total_text_conversation += f"Assistant: {assistant_message}\n"

        # return assistant_message, total_text_conversation

    def generate_response(prompt_input):
        system_prompt_content = construct_prompt("patient")
        system_prompt_content = system_prompt_content.replace("ADDITIONAL_INFORMATION", build_additional_information())

        # print("SYSTEM PROMPT ::: ", system_prompt_content)

        prompt = [{"role": "system", "content": system_prompt_content}] + st.session_state.conversation_messages[-2:] + [{"role": "user", "content": prompt_input}]
        
        # Add the system prompt to the total_text_conversation if it's not already there
        if not st.session_state.total_text_conversation.startswith("System: "):
            st.session_state.total_text_conversation = f"System: {system_prompt_content}\n" + st.session_state.total_text_conversation

        output, st.session_state.total_text_conversation = llm_generate_response(prompt, total_text_conversation=st.session_state.total_text_conversation)
        return output
    
    def generate_summary(conversation):
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")
        
        summary_prompt = [
            {"role": "system", "content": """You are a helpful assistant. Your task is to summarize the following conversation while retaining key information and context. 
             Generate a short summary of the patient description based on the conversation.
    Write as a doctor taking notes, using this format:
    - Patient
      - Sex, Age, Location, Recent travels, Occupation
    - Symptoms
      - [Symptom] Timing, Location, Pain level, Type of pain
    - Medical history
      - Personal, Family, Current medications, Medical tests.
             
  - Leave unknown fields blank
  - Exclude diagnostic or treatment information
  - Only include information from the conversation
  - Strictly adhere to the format
  - Don't add extra information"""},
            {"role": "user", "content": f"Please summarize the following conversation:\n\n{conversation}"}
        ]
        
        response = client.chat.completions.create(
            model="llama-3-70b-meditron",
            messages=summary_prompt,
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content

    # User-provided prompt
    if prompt := st.chat_input("How can I assist you today ?"):
        st.session_state.conversation_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    def estimate_tokens(text):
        return len(text) // 3.5

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

        print("Estimation of total tokens: ", estimate_tokens(st.session_state.total_text_conversation))

        # Check token count and summarize if necessary
        if estimate_tokens(st.session_state.total_text_conversation) > 3500:  # Lower threshold to allow room for summary
            # Extract the conversation part (excluding system prompt)
            system_prompt_end = st.session_state.total_text_conversation.find("\nUser: ")
            system_prompt = st.session_state.total_text_conversation[:system_prompt_end]
            conversation_to_summarize = st.session_state.total_text_conversation[system_prompt_end:]
            
            # Generate summary
            summary = generate_summary(conversation_to_summarize)
            
            # Replace the conversation with the summary
            st.session_state.total_text_conversation = f"{system_prompt}\n\nSummary of previous conversation:\n{summary}\n\nUser: {prompt}\nAssistant: {full_response}\n"
            
            print("SUMMARY ::: ", summary)

            # Update conversation_messages
            st.session_state.conversation_messages = [
                {"role": "system", "content": "Summary of previous conversation: " + summary},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": full_response}
            ]