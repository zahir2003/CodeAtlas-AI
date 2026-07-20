import logging
from pathlib import Path
from uuid import UUID

from git import GitCommandError, Repo

from app.storage.repository_manager import RepositoryManager

logger = logging.getLogger(__name__)


class CloneService:

    @staticmethod
    def clone_repository(
        clone_url: str,
        repository_id: UUID,
    ) -> Path:

        RepositoryManager.initialize()

        repo_path = RepositoryManager.get_repository_path(
            repository_id,
        )

        repo_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if repo_path.exists():

            logger.info(
                "Repository already exists | ID=%s",
                repository_id,
            )

            return repo_path

        try:

            logger.info(
                "Cloning repository | ID=%s",
                repository_id,
            )

            Repo.clone_from(
                clone_url,
                repo_path,
                depth=1,
                single_branch=True,
            )

            logger.info(
                "Repository cloned successfully | ID=%s",
                repository_id,
            )

            return repo_path

        except GitCommandError as e:

            logger.error(
                "Clone failed | ID=%s | Error=%s",
                repository_id,
                str(e),
            )

            raise
