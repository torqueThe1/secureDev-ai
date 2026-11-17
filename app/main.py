
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.rag.llm import generate_answer


app = FastAPI()



from typing import Literal


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    source: Literal[
        "all",
        "fastapi_oauth2_jwt.md",
        "owasp_authentication.md"
    ] = "all"
    history: list[ChatMessage] = Field(default_factory=list)



@app.get("/")
def home():
    return {"message": "Welcome to SecureDev AI!"}





@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    selected_source = (
        None if request.source == "all"
        else request.source
    )

    history = [
        message.model_dump()
        for message in request.history
    ]

    result = generate_answer(
        question=request.question,
        source=selected_source,
        include_sources=True,
        history=history
    )

    return result

