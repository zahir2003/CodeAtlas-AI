from pydantic import BaseModel


class SearchResult(BaseModel):

    score: float

    chunk_id: str

    repository_id: int

    path: str

    content: str