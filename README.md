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
