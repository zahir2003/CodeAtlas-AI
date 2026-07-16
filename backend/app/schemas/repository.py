from pydantic import BaseModel, HttpUrl


class RepositoryCreate(BaseModel):
    github_url: HttpUrl