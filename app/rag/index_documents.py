
from pathlib import Path

from app.rag.chunk_documents import split_text, split_python_code
from app.rag.vector_store import collection


def index_documents():
    data_dir = Path("data/processed")

    for file_path in sorted(data_dir.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        chunks = split_text(text)

        if file_path.name == "fastapi_oauth2_jwt.md":
            example_path = Path("data/raw/fastapi_jwt_example.py")

            if not example_path.exists():
                raise FileNotFoundError(example_path)

            example_code = example_path.read_text(encoding="utf-8")
            code_chunks = split_python_code(example_code)

            chunks.extend(code_chunks)

        ids = [
            f"{file_path.stem}_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {"source": file_path.name, "chunk_index": i}
            for i in range(len(chunks))
        ]

        # Remove outdated chunks before reindexing this source
        collection.delete(where={"source": file_path.name})

        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )

        print(f"Indexed {len(chunks)} chunks from {file_path.name}")

    print(f"Total stored chunks: {collection.count()}")


if __name__ == "__main__":
    index_documents()
