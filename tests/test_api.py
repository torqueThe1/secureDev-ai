
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_rejects_invalid_source():
    response = client.post(
        "/chat",
        json={
            "question": "What is JWT?",
            "source": "invalid_source"
        }
    )

    assert response.status_code == 422


def test_chat_rejects_empty_question():
    response = client.post(
        "/chat",
        json={
            "question": "",
            "source": "all"
        }
    )

    assert response.status_code == 422


def test_chat_accepts_valid_request():
    from unittest.mock import patch

    mock_result = {
        "answer": "JWT is a JSON Web Token.",
        "sources": []
    }

    with patch(
        "app.main.generate_answer",
        return_value=mock_result
    ) as mock_generate:
        response = client.post(
            "/chat",
            json={
                "question": "What is JWT?",
                "source": "fastapi_oauth2_jwt.md"
            }
        )

    assert response.status_code == 200
    assert response.json() == mock_result

    mock_generate.assert_called_once_with(
        question="What is JWT?",
        source="fastapi_oauth2_jwt.md",
        include_sources=True,
        history=[]
    )


def test_chat_passes_conversation_history():
    from unittest.mock import patch

    history = [
        {
            "role": "user",
            "content": "What is JWT?"
        },
        {
            "role": "assistant",
            "content": "JWT stands for JSON Web Token."
        }
    ]

    mock_result = {
        "answer": "JWT signatures can be verified using PyJWT.",
        "sources": []
    }

    with patch(
        "app.main.generate_answer",
        return_value=mock_result
    ) as mock_generate:
        response = client.post(
            "/chat",
            json={
                "question": "How is it verified?",
                "source": "all",
                "history": history
            }
        )

    assert response.status_code == 200

    mock_generate.assert_called_once_with(
        question="How is it verified?",
        source=None,
        include_sources=True,
        history=history
    )
