
# SecureDev AI

SecureDev AI is a local, retrieval-augmented generation (RAG) chatbot for secure software development.

It answers questions using FastAPI security documentation and the OWASP Authentication Cheat Sheet.

## Features

- Semantic document search using ChromaDB
- AI-generated answers using Ollama and Gemma 3
- FastAPI and OWASP knowledge source filtering
- Retrieved document references for each answer
- Conversation history support
- Original Python code examples from the documentation
- Interactive Streamlit chat interface
- Automated API and code-chunking tests

## Technology Stack

- Python 3.13
- FastAPI
- Streamlit
- ChromaDB
- Ollama (Gemma 3 4B)
- Pytest

## Requirements

- Python 3.13
- Ollama installed locally
- The `gemma3:4b` model downloaded
- Project dependencies installed in a Python virtual environment

Download the language model:

    ollama pull gemma3:4b

## Running the Application

Start the FastAPI backend:

    .\.venv313\Scripts\python.exe -m uvicorn app.main:app --reload

In a separate terminal, start Streamlit:

    .\.venv313\Scripts\python.exe -m streamlit run streamlit_app.py

Open the local Streamlit URL displayed in the terminal.

## Document Indexing

The application uses processed Markdown documents and a local ChromaDB collection.

To rebuild the vector database:

    .\.venv313\Scripts\python.exe -m app.rag.index_documents

The indexing process also includes Python implementation examples from the FastAPI documentation.

## Testing

Run the automated tests:

    .\.venv313\Scripts\python.exe -m pytest tests -v

## Limitations

- The application runs locally and requires Ollama.
- Answers depend on the available documentation.
- AI-generated code may contain errors and should be reviewed before use.
- Original code examples may require additional imports and dependencies.

## Documentation Sources

- FastAPI OAuth2 with JWT tutorial
- OWASP Authentication Cheat Sheet
