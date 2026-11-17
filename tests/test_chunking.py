
from app.rag.chunk_documents import split_python_code


def test_python_functions_remain_complete():
    sample_code = """
def create_access_token(data):
    token = data.copy()
    return token


async def get_current_user(token):
    username = token.get("sub")
    return username
"""

    chunks = split_python_code(sample_code)

    assert len(chunks) == 2

    assert chunks[0].startswith("def create_access_token")
    assert "return token" in chunks[0]

    assert chunks[1].startswith("async def get_current_user")
    assert "return username" in chunks[1]
