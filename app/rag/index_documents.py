
from pathlib import Path

from app.rag.chunk_documents import split_text
from app.rag.vector_store import collection


def index_documents():
    data_dir = Path("data/processed")

    for file_path in sorted(data_dir.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        chunks = split_text(text)

        ids = [
            f"{file_path.stem}_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {"source": file_path.name, "chunk_index": i}
            for i in range(len(chunks))
        ]

        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )

        print(f"Indexed {len(chunks)} chunks from {file_path.name}")

    print(f"Total stored chunks: {collection.count()}")


if __name__ == "__main__":
    index_documents()
