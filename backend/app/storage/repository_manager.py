from pathlib import Path

from app.core.constants import REPOSITORY_STORAGE


class RepositoryManager:

    STORAGE_ROOT = Path(REPOSITORY_STORAGE)

    @classmethod
    def initialize(cls):

        cls.STORAGE_ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

    @classmethod
    def repository_path(
        cls,
        repository_id: int,
    ) -> Path:

        return cls.STORAGE_ROOT / str(repository_id)

    @classmethod
    def repository_exists(
        cls,
        repository_id: int,
    ) -> bool:

        return cls.repository_path(repository_id).exists()