from pydantic import BaseModel


class Document(BaseModel):
    repository_id: int

    path: str

    language: str

    extension: str

    size: int

    content: str