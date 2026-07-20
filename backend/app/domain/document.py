from pydantic import BaseModel
from uuid import UUID

class Document(BaseModel):
    repository_id: UUID
    path: str
    language: str
    extension: str
    size: int
    content: str
