from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.sentinel import agent


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@router.post("/chat")
def chat(request: ChatRequest):

    response = agent.chat(
        message=request.message,
        session_id=request.session_id
    )

    return {
        "response": response
    }