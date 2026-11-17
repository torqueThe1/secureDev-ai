
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

    # Include previous questions in document retrieval
    previous_questions = [
        message["content"]
        for message in recent_history
        if message["role"] == "user"
    ]

    search_query = " ".join(
        previous_questions[-2:] + [question]
    )

    results = retrieve_documents(
        search_query,
        source=source
    )

    documents = results["documents"][0]
    context = "\n\n---\n\n".join(documents)

    system_prompt = """
    You are SecureDev AI, a secure software development assistant.

    Answer using only the provided documentation context.
    Use conversation history to understand follow-up questions.
    Previous assistant responses are not evidence.

    Do not invent information.
    If the context is insufficient, say so clearly.

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

    if include_sources:
        sources = [
            {
                "file": metadata["source"],
                "chunk_index": metadata["chunk_index"]
            }
            for metadata in results["metadatas"][0]
        ]

        return {
            "answer": answer,
            "sources": sources
        }

    return answer
