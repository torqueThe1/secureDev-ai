
from app.rag.vector_store import collection


def retrieve_documents(
    question: str,
    top_k: int = 5,
    source: str | None = None
):
    query_params = {
        "query_texts": [question],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }

    if source is not None:
        query_params["where"] = {"source": source}

    return collection.query(**query_params)
