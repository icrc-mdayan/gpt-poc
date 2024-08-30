import streamlit as st
from abc import ABC
from scripts.utils import construct_prompt
from lib.agents.llm_agent import LLMAgent
import yaml

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

def run_conversation_patient_v2():
    st.title('Conversation-Patient 💬')

    st.subheader('Instructions :')

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

    st.subheader('Patient Information :')
    col1, col2 = st.columns(2)
    
    with col1:
        Sex = st.selectbox('Sex', ('Male', 'Female', 'Other'), key='Sex')
        location = st.text_input('Location/Region', key='location', placeholder='City, Country')
    
    with col2:
        age = st.number_input('Age', min_value=0, max_value=120, key='age', placeholder='-')
        travel_history = st.text_input('Recent travel places', key='travel_history', placeholder='City, Country')

    if "conversation_messages" not in st.session_state:
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    for message in st.session_state.conversation_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    total_text_conversation = ""

    def clear_chat_history():
        st.session_state.conversation_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.session_state['location'] = ''
        st.session_state['age'] = None
        st.session_state['Sex'] = 'Male'
        st.session_state['travel_history'] = ''

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def generate_response_from_llm(user_prompt, total_text_conversation):

        print("Start generating response from LLM...")

        conversation_agent = LLMAgent(agent_name="medical_assistant_conversation", model_name="llama-3-70b-meditron", system_prompt=construct_prompt("patient"), total_text_conversation=total_text_conversation)
        
        # only take the dict where role = user instead of whole the st.session_state.conversation_message
        user_answers = [{"role": "user", "content": message["content"]} for message in st.session_state.conversation_messages if message["role"] == "user"]

        patient_description = update_patient_description(user_answers, build_additional_information())
        
        prompt = conversation_agent.prepare_prompt(user_prompt, patient_description)
        response, total_text_conversation = conversation_agent.generate_response(prompt)

        print("------ PROMPT CONVERSATION ------")
        print(prompt)
        print("---------------------------------")

        print("Finish generating response from LLM!")

        diagnostic_response = None

        # print("------ DIAGNOSTIC IN PROGRESS ------")
        # with open("prompts/conversation/config_prompts_diagnostic.yaml", "r") as file:
        #     yaml_content = yaml.safe_load(file)
        # diagnostic_prompt = yaml_content["diagnostic_prompt"]        
        # diagnostic_agent = LLMAgent(agent_name="medical_assistant_diagnostic", model_name="llama-3-70b-meditron", system_prompt=diagnostic_prompt)
        # prompt_diagnostic = diagnostic_agent.prepare_prompt(None, patient_description)
        # diagnostic_response = diagnostic_agent.generate_response(prompt_diagnostic)
        # print("------ PROMPT DIAGNOSTIC ------")
        # print(prompt_diagnostic)
        # print("------ DIAGNOSTIC FINISHED ------")

        return response, diagnostic_response, total_text_conversation
    
    def update_patient_description(chat_history, additional_information):

        print("Start summarizing the patient description...")

        with open("prompts/conversation/config_prompts_summarizer.yaml", "r") as file:
            yaml_content = yaml.safe_load(file)
        
        system_prompt_summarizer = yaml_content["patient_decription_summarizer"]
        summarizer_agent = LLMAgent(agent_name="summarizer", model_name="llama-3-70b-meditron", system_prompt=system_prompt_summarizer, total_text_conversation="")

        chats = " ".join([message["content"] for message in chat_history])

        prompt = [{"role": "system", "content": system_prompt_summarizer}, {"role": "user", "content": additional_information + chats}]
        updated_patient_description, _ = summarizer_agent.generate_response(prompt)

        # print("Finish summarizing the patient description!")

        # print("------ PROMPT SUMMARIZER ------")
        # print(prompt)
        # print("-------------------------------")

        # print("------ Updated Patient Description ------")
        # print(updated_patient_description)
        # print("-----------------------------------------")

        # updated_patient_description = "**Patient**\n" + updated_patient_description.split("Patient")[1].strip()
        return updated_patient_description
    
    def estimate_tokens(text):
        return len(text) // 3.5

    if prompt := st.chat_input("How can I assist you today ?"):
        st.session_state.conversation_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.conversation_messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, diagnostic, awesom = generate_response_from_llm(st.session_state.conversation_messages[-1]["content"], total_text_conversation=total_text_conversation)
                print("$$$ The number of tokens is estimated to be: ", estimate_tokens(total_text_conversation), " $$$")
                placeholder = st.empty()
                placeholder.markdown(response)
        message = {"role": "assistant", "content": response}
        st.session_state.conversation_messages.append(message)
