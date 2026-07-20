from uuid import UUID
from pydantic import BaseModel


class ChatRequest(BaseModel):
    repository_id: UUID
    session_id: str
    question: str
    top_k: int = 5


class SourceChunk(BaseModel):
    file_path: str
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
