from pydantic import BaseModel
from uuid import UUID

class SearchResult(BaseModel):

    score: float

    chunk_id: str

    repository_id: UUID

    path: str

    content: str
