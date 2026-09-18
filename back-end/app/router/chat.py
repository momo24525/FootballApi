from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import process_chat

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    return {
        "response": process_chat(
            question=request.question,
            matches=request.matches
        )
    }