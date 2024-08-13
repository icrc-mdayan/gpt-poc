import streamlit as st
from openai import OpenAI
from retriever.embedding import Vectorstore
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import voyageai
from nltk.tokenize import sent_tokenize
from scipy.spatial.distance import cosine
import nltk
import os
from streamlit_pdf_viewer import pdf_viewer
import streamlit.components.v1 as components
from urllib.parse import quote
import json

# Custom function to embed PDF using PDF.js
def pdf_viewer(url):
    pdf_js_html = f"""
    <iframe src="pdfjs/web/viewer.html?file={url}" width="100%" height="600px" style="border:none;"></iframe>
    """
    components.html(pdf_js_html, height=600)


data_dir = os.path.join(os.getcwd(), 'data')
nltk.data.path.append(data_dir)

def _split_sentences(text):
    # Use regular expressions to split the text into sentences based on punctuation followed by whitespace.
    sentences = sent_tokenize(text)
    return sentences

def convert_to_vector(texts):
    # Try to generate embeddings for a list of texts using a pre-trained model and handle any exceptions.
    try:
        voyageai.api_key = "pa-dQ28MnYTDY5xF72HnbBVB5-w9FCs7E6yzzZBbAn0YPk"
        vo = voyageai.Client()
        embeddings = []
        # Je devrais pas faire doc par doc, mais faire par batch et après ajouter chaque embedded document dans documents_embeddings
        for i in range(0, len(texts), 100):
            embed = vo.embed(texts[i:i+100], model="voyage-large-2-instruct", input_type="document").embeddings
            for emb in embed:
                embeddings.append(emb) 
        # embeddings = np.array([item.embedding for item in response.data])
        return embeddings
    except Exception as e:
        print("An error occurred:", e)
        return np.array([])  # Return an empty array in case of an error

def find_closest_sentence(query_embedding, sentences, sentence_embeddings):
    min_distance = float('inf')
    closest_sentence = sentences[0]
    for sentence, embedding in zip(sentences, sentence_embeddings):
        distance = cosine(query_embedding[0], embedding)
        if distance < min_distance:
            min_distance = distance
            closest_sentence = sentence
    return closest_sentence

def run_rag_mode():
    # Page title for RAG-mode
    st.title('ICRC-knowledge based chatbot')
    st.write(
        """
        <div style="padding: 10px;">
            This model uses Retrieval-Augmented Generation (RAG) to generate responses based on the ICRC and MSF knowledge base. It is able to read documents and generate reponses based on the information it has read.
        </div>
        """, unsafe_allow_html=True)

    st.write(
        """
        <div style="padding: 5px;">
            For now, the knowledge base only consists of 4 books: 
            <b>MSF Guidelines</b>, 
            <b>ICRC War Surgery Guidelines</b>, 
            <b>ICRC Nursing Guidelines</b>, and 
            <b>MSF Newborn Care Guidelines</b>. 
            Feel free to suggest more resources that are useful to you.
        </div>
        """, unsafe_allow_html=True)

                
    
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
        response = client.chat.completions.create(model="llama-3-70b-meditron", messages=prompt_input)
        return response.choices[0].message.content

    def generate_response(prompt_input, vectore_store):
        with open("prompts/system_prompt_rag.txt", 'r') as file:
            system_prompt = file.read().strip()

        documents, query_embedding = vectore_store.retrieve_documents(prompt_input)

        if documents:
            st.markdown(
                """
                <style>
                    .css-18e3th9 {
                        flex-direction: row-reverse;
                    }
                    .document-title {
                        color: #2E8B57;
                        font-size: 24px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }
                    .highlight {
                        font-weight: bold;
                    }
                    .stSidebar {
                        background-color: #F0F0F0;
                        padding: 20px;
                        border-radius: 10px;
                    }
                    .custom-expander .st-expander-header p {
                        color: #2E8B57 !important;
                        font-size: 20px !important;
                        font-weight: bold !important;
                    }
                </style>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        let expanders = document.querySelectorAll(".st-expander");
                        expanders.forEach(function(expander) {
                            let header = expander.querySelector(".st-expander-header");
                            if (header) {
                                header.style.fontSize = "24px";
                                header.style.fontWeight = "bold";
                                header.style.color = "#2E8B57";
                            }
                        });
                    });
                </script>
                """,
                unsafe_allow_html=True,
            )

            with st.sidebar:
                st.write("## Retrieved Documents")
                for idx, doc in enumerate(documents, start=1):
                    # Extract the title from the document
                    # source_match = re.search(r"^\*\*(.*?)\*\*", doc)
                    # source = source_match.group(1) if source_match else "Unknown Source"

                    # title_match = re.search(r"^#{1,2}\s*(.*)", doc, re.MULTILINE)
                    # title = title_match.group(1) if title_match else f"Document {idx}"
                    source = doc["source_document"]
                    title = doc["paragraph_title"]
                    if doc["subtitle"] is not None:
                        title += f" - {doc['subtitle']}"
                    # Construct the PDF file path
                    encoded_source = quote(source)
                    pdf_path = f"https://media.githubusercontent.com/media/icrc-mdayan/gpt-poc/main/retriever/ressources/{encoded_source}.pdf"
                    
                    # Remove the title from the document content
                    #content = re.sub(r"^\*\*.*?\*\*\s*|^#{1,2}\s*.*\n", '', doc, flags=re.MULTILINE).strip()
                    content = doc["text"]
                    sentences = _split_sentences(content)
                    sentence_embeddings = convert_to_vector(sentences)
                    
                    # Find the closest sentence to the query
                    closest_sentence = find_closest_sentence(query_embedding, sentences, sentence_embeddings)
                    
                    # Highlight the closest sentence
                    highlighted_doc = content.replace(closest_sentence, f'<span class="highlight">{closest_sentence}</span>')
                    
                    # Using simple expander title and styled title inside the expander
                    with st.expander(f"from: {source}, paragraph: {title}"):
                        
                        st.markdown(f'You can check the source at: {pdf_path}', unsafe_allow_html=True)
                        
                        st.markdown(f'<div class="document-content">{highlighted_doc}</div>', unsafe_allow_html=True)
                        pdf_viewer_url = f"/static/pdfjs/web/viewer.html?file={pdf_path}"
                        st.components.v1.html(f'<iframe src="{pdf_viewer_url}" width="100%" height="600px" style="border:none;"></iframe>', height=600)

                        
                        

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
    with open('retriever/books_embeddings_2.jsonl', 'r') as json_file:
            documents_embeddings = json.load(json_file)
    data = []
    with open('retriever/books_split_final.jsonl', 'r') as json_file:
        for line in json_file:
            data.append(json.loads(line))
    shape = 1024
    vectore_store = Vectorstore(document_embeddings=documents_embeddings, data=data, shape=shape)
    # Generate a new response if last message is not from assistant
    if st.session_state.rag_messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            st.spinner("Thinking...")
            response = generate_response(prompt, vectore_store)
            placeholder = st.empty()
            placeholder.markdown(response)
            
            # Update the session state with the assistant's response
            message = {"role": "assistant", "content": response}
            st.session_state.rag_messages.append(message)      
                   