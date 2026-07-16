from pydantic import BaseModel, HttpUrl


class RepositoryCreate(BaseModel):
    github_url: HttpUrl


class RepositoryResponse(BaseModel):
    submitted_url: HttpUrl
    canonical_url: HttpUrl
    redirected: bool

    repository_name: str
    owner: str

    description: str | None = None
    language: str | None = None

    stars: int
    forks: int

    default_branch: str

    visibility: str

    clone_url: HttpUrl