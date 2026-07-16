from fastapi import HTTPException

from app.schemas.repository import RepositoryCreate
from app.clients.github_client import GitHubClient
from app.utils.github_validator import is_valid_github_repo


class RepositoryService:

    @staticmethod
    async def create_repository(repository: RepositoryCreate):

        github_url = str(repository.github_url)

        if not is_valid_github_repo(github_url):
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub Repository URL."
            )

        repo = await GitHubClient.get_repository(github_url)

        if repo is None:
            raise HTTPException(
                status_code=404,
                detail="Repository not found."
            )

        return {
            "repository_name": repo["name"],
            "owner": repo["owner"]["login"],
            "description": repo["description"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "default_branch": repo["default_branch"],
            "visibility": "Public",
            "clone_url": repo["clone_url"]
        }