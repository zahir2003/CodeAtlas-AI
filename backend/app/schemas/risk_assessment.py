from pydantic import BaseModel


class RepositoryRiskAssessment(BaseModel):
    repository_size_mb: float
    estimated_clone_time_seconds: int
    estimated_index_time_seconds: int

    has_readme: bool
    has_license: bool

    archived: bool
    disabled: bool

    risk_level: str