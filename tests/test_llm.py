
from unittest.mock import patch

from app.rag.llm import generate_answer


def test_original_code_is_preserved():
    original_code = (
        "def authenticate_user(db, username):\n"
        "    return db[username]"
    )

    fake_results = {
        "documents": [[original_code]],
        "metadatas": [[{
            "source": "fastapi_oauth2_jwt.md",
            "chunk_index": 22
        }]]
    }

    with patch(
        "app.rag.llm.retrieve_documents",
        return_value=fake_results
    ), patch("app.rag.llm.chat") as mock_chat:

        mock_chat.return_value.message.content = (
            "The function returns the user object."
        )

        result = generate_answer(
            question="Show me code for user authentication",
            include_sources=True
        )

    assert result["answer"] == (
        "The function returns the user object."
    )

    assert result["code_examples"][0]["code"] == original_code
