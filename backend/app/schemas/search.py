from uuid import UUID

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    repository_id: UUID
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class SearchMatch(BaseModel):
    score: float
    repository_id: str
    file_path: str
    language: str
    extension: str | None = None
    chunk_index: int
    start_char: int | None = None
    end_char: int | None = None
    code: str


class SearchResponse(BaseModel):
    repository_id: UUID
    query: str
    total_matches: int
    matches: list[SearchMatch]
