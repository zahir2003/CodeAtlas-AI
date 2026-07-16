from fastapi import HTTPException

from app.schemas.repository import RepositoryCreate
from app.utils.github_validator import is_valid_github_repo


class RepositoryService:

    @staticmethod
    def create_repository(repository: RepositoryCreate):

        github_url = str(repository.github_url)

        if not is_valid_github_repo(github_url):
            raise HTTPException(
                status_code=400,
                detail="Please provide a valid public GitHub repository URL."
            )

        return {
            "message": "Repository validated successfully.",
            "repository_url": github_url
        }