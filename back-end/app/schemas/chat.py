from typing import Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    matches: list[dict[str, Any]]
    
class ChatResponse(BaseModel):
    response: str