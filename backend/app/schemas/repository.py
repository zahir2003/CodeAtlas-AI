from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl

from app.schemas.risk_assessment import RepositoryRiskAssessment


class RepositoryCreate(BaseModel):
    github_url: HttpUrl


class RepositoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    repository_id: UUID

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

    risk_assessment: RepositoryRiskAssessment
