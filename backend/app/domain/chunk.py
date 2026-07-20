from pydantic import BaseModel
from uuid import UUID

class Chunk(BaseModel):
    repository_id: UUID

    path: str

    language: str

    chunk_type: str

    symbol: str | None = None

    start_line: int

    end_line: int

    content: str
