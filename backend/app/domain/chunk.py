from pydantic import BaseModel


class Chunk(BaseModel):
    repository_id: int

    path: str

    language: str

    chunk_type: str

    symbol: str | None = None

    start_line: int

    end_line: int

    content: str