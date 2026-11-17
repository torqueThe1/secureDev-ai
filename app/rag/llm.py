
from ollama import chat

from app.rag.retriever import retrieve_documents


MODEL_NAME = "gemma3:4b"


def generate_answer(
    question: str,
    source: str | None = None,
    include_sources: bool = False,
    history: list[dict[str, str]] | None = None
) -> str | dict:

    # Keep the last 6 conversation messages
    recent_history = (history or [])[-6:]

    # Include previous user questions in retrieval
    previous_questions = [
        message["content"]
        for message in recent_history
        if message["role"] == "user"
    ]

    search_query = " ".join(
        previous_questions[-2:] + [question]
    )

    # Retrieve relevant documentation
    results = retrieve_documents(
        search_query,
        top_k=12,
        source=source
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Prioritize Python functions in the context
    code_examples = [
        document
        for document in documents
        if document.lstrip().startswith(
            ("def ", "async def ", "class ", "@")
        )
    ]

    explanations = [
        document
        for document in documents
        if not document.lstrip().startswith(
            ("def ", "async def ", "class ", "@")
        )
    ]

    context = "\n\n---\n\n".join(
        code_examples + explanations
    )

    # Prepare document references
    sources = [
        {
            "file": metadata["source"],
            "chunk_index": metadata["chunk_index"]
        }
        for metadata in metadatas
    ]

    # Preserve original Python code
    original_code_examples = [
        {
            "file": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "code": document
        }
        for document, metadata in zip(
            documents,
            metadatas
        )
        if document.lstrip().startswith(
            ("def ", "async def ", "class ", "@")
        )
    ]

    # Detect implementation-related questions
    is_code_question = any(
        keyword in question.lower()
        for keyword in ("code", "implement", "function")
    )

    if is_code_question and original_code_examples:

        # Explain original functions without rewriting them
        explanation_response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SecureDev AI. "
                        "Explain the retrieved Python functions "
                        "briefly and accurately. "
                        "Use only the provided source code. "
                        "Address the user's actual question. "
                        "Do not generate, rewrite, or modify Python code. "
                        "Do not invent missing implementation details. "
                        "Describe function return values exactly "
                        "as they appear in the source code. "
                        "Distinguish between returning a user object "
                        "and returning a boolean value. "
                        "Do not assume that successful authentication "
                        "always returns True. "
                        "Always respond in English."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Question:\n{question}\n\n"
                        "Original Python functions:\n\n"
                        + "\n\n---\n\n".join(
                            example["code"]
                            for example in original_code_examples
                        )
                    )
                }
            ],
            options={"temperature": 0.2}
        )

        answer = explanation_response.message.content or ""

    else:

        # Answer normal questions using the RAG context
        system_prompt = """
        You are SecureDev AI, a secure software development assistant.

        Answer using only the provided documentation context.
        Use conversation history to understand follow-up questions.
        Previous assistant responses are not evidence.

        Explain concepts clearly and accurately.
        Do not invent information or unsupported code.
        Do not copy unrelated documentation sections.

        If the documentation is insufficient,
        clearly state what information is missing.

        Always respond in English.
        """

        user_prompt = f"""
        Documentation Context:
        {context}

        Current Question:
        {question}
        """

        response = chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                *recent_history,
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0.2}
        )

        answer = response.message.content or ""

    # Return answer with sources and original code
    if include_sources:
        return {
            "answer": answer,
            "sources": sources,
            "code_examples": original_code_examples
        }

    return answer
