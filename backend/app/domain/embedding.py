from pydantic import BaseModel


class Embedding(BaseModel):

    chunk_id: str

    vector: list[float]

    metadata: dict