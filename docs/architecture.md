\# SecureDev AI - System Architecture



\## Overview

A RAG-based chatbot for secure software development.



\## Main Components

\- Frontend: Streamlit

\- Backend: FastAPI

\- Vector Database: ChromaDB

\- Knowledge Sources: FastAPI and OWASP documentation

\- Language Model: To be selected



\## RAG Workflow

User Question -> Document Retrieval -> LLM -> Answer with Sources





\## Document Processing Pipeline



1\. Collect FastAPI and OWASP documentation.

2\. Extract and clean document text.

3\. Split text into smaller chunks.

4\. Generate embeddings for each chunk.

5\. Store embeddings and metadata in ChromaDB.

6\. Retrieve relevant chunks for user questions.

7\. Generate an answer with source references.





\## API Design



\### POST /chat



Receives a user question and returns an AI-generated answer

based on retrieved documentation.



Request:

{

&#x20; "question": "How can I secure a FastAPI endpoint?"

}



Response:

{

&#x20; "answer": "Generated answer based on documentation.",

&#x20; "sources": \[

&#x20;   {

&#x20;     "title": "OWASP Documentation",

&#x20;     "url": "https://cheatsheetseries.owasp.org/"

&#x20;   }

&#x20; ]

}



