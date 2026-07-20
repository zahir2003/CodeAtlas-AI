from pathlib import Path
from shutil import rmtree
from uuid import UUID

from app.core.config import REPOSITORIES_DIR


class RepositoryManager:
    """Manage temporary local repository storage."""

    @classmethod
    def initialize(cls) -> None:
        """Create the base repositories directory if it doesn't exist."""
        REPOSITORIES_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    @classmethod
    def get_repository_path(
        cls,
        repository_id: UUID,
    ) -> Path:
        """Return the repository path without creating it."""
        return REPOSITORIES_DIR / str(repository_id)

    @classmethod
    def repository_exists(
        cls,
        repository_id: UUID,
    ) -> bool:
        """Check whether the repository has already been cloned."""
        return cls.get_repository_path(repository_id).exists()

    @classmethod
    def delete_repository(
        cls,
        repository_id: UUID,
    ) -> None:
        """Delete the temporary cloned repository."""
        repo_path = cls.get_repository_path(repository_id)

        if repo_path.exists():
            rmtree(repo_path)
