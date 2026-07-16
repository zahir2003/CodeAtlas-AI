from app.schemas.repository import RepositoryCreate


class RepositoryService:

    @staticmethod
    def create_repository(repository: RepositoryCreate):

        return {
            "message": "Repository received successfully",
            "repository_url": str(repository.github_url)
        }