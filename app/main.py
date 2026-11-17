
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.rag.llm import generate_answer


app = FastAPI()


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)


@app.get("/")
def home():
    return {"message": "Welcome to SecureDev AI!"}


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    answer = generate_answer(request.question)

    return {"answer": answer}
