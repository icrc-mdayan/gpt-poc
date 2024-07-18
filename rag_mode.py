import streamlit as st
from openai import OpenAI
from retriever.embedding import retrieve_documents

def run_rag_mode():
    # Page title for RAG-mode
    st.title('RAG-mode')

    # Store LLM generated responses
    if "rag_messages" not in st.session_state.keys():
        st.session_state.rag_messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.rag_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    def llm_generate_response(prompt_input):
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")
        response = client.chat.completions.create(model="llama-2-70b-meditron", messages=prompt_input)
        return response.choices[0].message.content

    def generate_response(prompt_input):
        with open("prompts/system_prompt_rag.txt", 'r') as file:
            system_prompt = file.read().strip()
        #prompt.append({"role": "user", "content": prompt_input})
        documents = retrieve_documents(prompt_input)
        if documents != []:
            with st.sidebar:
                st.write("## Retrieved Documents")
                for idx, doc in enumerate(documents, start=1):
                    with st.expander(f"Document {idx}"):
                        st.write(doc)  

            # Now generate the response using the documents (if necessary) and prompt
            question = [{"role": "system", "content": system_prompt}]
            question.extend(st.session_state.rag_messages[:-1])
            formatted_documents = "\n".join([f"Document {idx+1}:\n{doc}" for idx, doc in enumerate(documents)])
            question.append({"role": "user", "content": f"{formatted_documents}\n\nQuestion: {prompt_input}"})
            output = llm_generate_response(question)
        else:
            output = llm_generate_response(st.session_state.rag_messages)

        return output

    # User-provided prompt
    if prompt := st.chat_input("How can I help you?"):
        st.session_state.rag_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.rag_messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                placeholder = st.empty()
                full_response = response
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.rag_messages.append(message)
