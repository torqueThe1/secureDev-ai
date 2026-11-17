
from ollama import chat

from app.rag.retriever import retrieve_documents


MODEL_NAME = "gemma3:4b"


def generate_answer(question: str) -> str:
    results = retrieve_documents(question)

    documents = results["documents"][0]

    context = "\n\n---\n\n".join(documents)

    system_prompt = """
    You are SecureDev AI, a secure software development assistant.

    Answer the user's question using only the provided context.
    Do not invent information that is not in the documentation.
    If the context is insufficient, clearly state that you
    cannot answer based on the available documentation.

    Always respond in English.
    """

    user_prompt = f"""
    Context:
    {context}

    Question:
    {question}
    """

    response = chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        options={"temperature": 0.2}
    )

    return response.message.content or ""
