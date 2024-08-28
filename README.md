# streamlit_icrc

## Introduction
- This repo presents proofs of concept (POC) of two features that aim to be integrated into the MOOVE platform in the future.
- The RAG feature offers a Retriever Augmented Generation that fetches additional context from a database of medical guidelines to help Meditron-3 give more accurate and relevant answers. It also displays the sources of the retrieved documents to maintain good explainability.
- The Conversational feature offers a version of Meditron-3 tailored for conversational use. The model asks questions mimicking a doctor, to better understand the patient case and give a differential diagnosis.

## Getting Started
- To get started, if you have cloned the repo and want to run this locally, install the dependencies using the following command:

    ```bash
    pip install -r requirements.txt
    ```

    Then run this command:

    ```bash
    streamlit run main.py
    ```

- If you want to access this online from a browser, click on the following link: [Streamlit App](https://healthpoc.streamlit.app/)


## Setting up RAG Mode
If you want to use RAG Mode you need to setup a cohere and voyageai account (they are free) and put your API keys in API_token.json

## Modifying base documents for RAG Mode

If you want to embed new documents you can run the embedding.py script with the following command:
 
    ```bash
    python3 retriever\embedding.py your_file.jsonl new_embeddings_file.jsonl
    ```
This will create a new embedding file.
You then need to change the files at line 77 and 80 in main.py to put your embedding and documents files

note:
The format of the documents needs to be:
    ```bash
    {"source_document": , "page_number": , "paragraph_title": , "subtitle": , "text": }
    ```
You should also put the source documents in the 'retriever\ressources' folder if you want the user to be able to check at the source document. 

note 2:
If you want to use semantic chunking you can use the chunk_text function from documents\data_splitting.py