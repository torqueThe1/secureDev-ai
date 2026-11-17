
from app.rag.vector_store import collection


def retrieve_documents(question: str, top_k: int = 5):
    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results
