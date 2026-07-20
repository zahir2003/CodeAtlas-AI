from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.clients.github_client import GitHubClient
from app.crud.repository import RepositoryCRUD
from app.db.database import SessionLocal
from app.models.repository import (
    Repository,
    RepositoryStatus,
)
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.clone_service import CloneService
from app.services.indexing_service import IndexingService
from app.services.risk_assessment_service import RiskAssessmentService
from app.storage.repository_manager import RepositoryManager


class RepositoryService:
    """Business logic for repository operations."""

    def __init__(self):
        self.clone = CloneService()
        self.index = IndexingService()

    async def create_repository(
        self,
        db: Session,
        repository: RepositoryCreate,
    ) -> RepositoryResponse:
        """
        Register a GitHub repository.

        Steps:
        1. Check duplicate repository.
        2. Fetch GitHub metadata.
        3. Fetch repository contents.
        4. Assess repository risk.
        5. Save repository.
        6. Return response.
        """

        github_url = str(repository.github_url)

        existing = RepositoryCRUD.get_by_github_url(
            db,
            github_url,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Repository already exists.",
            )

        repo = await GitHubClient.get_repository(github_url)

        if repo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repository not found.",
            )

        contents = await GitHubClient.check_repository_files(
            github_url,
        )

        risk = RiskAssessmentService.assess(
            repo,
            contents,
        )

        db_repository = Repository(
            github_url=github_url,
            canonical_url=repo["html_url"],
            redirected=False,
            repository_name=repo["name"],
            owner=repo["owner"]["login"],
            description=repo.get("description"),
            language=repo.get("language"),
            stars=repo["stargazers_count"],
            forks=repo["forks_count"],
            visibility=repo["visibility"],
            clone_url=repo["clone_url"],
            default_branch=repo["default_branch"],
            latest_commit=None,
        )

        db_repository = RepositoryCRUD.create(
            db,
            db_repository,
        )

        return RepositoryResponse(
            repository_id=db_repository.id,
            submitted_url=repository.github_url,
            canonical_url=db_repository.canonical_url,
            redirected=db_repository.redirected,
            repository_name=db_repository.repository_name,
            owner=db_repository.owner,
            description=db_repository.description,
            language=db_repository.language,
            stars=db_repository.stars,
            forks=db_repository.forks,
            default_branch=db_repository.default_branch,
            visibility=db_repository.visibility,
            clone_url=db_repository.clone_url,
            risk_assessment=risk,
        )

    async def process_repository(
        self,
        repository_id: UUID,
    ):
        """
        Complete repository processing pipeline.

        PENDING
            ↓
        CLONING
            ↓
        INDEXING
            ↓
        READY
        """

        db = SessionLocal()

        try:
            repository = RepositoryCRUD.get_by_id(
                db,
                repository_id,
            )

            if repository is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Repository not found.",
                )

            # Step 1 - Update status to CLONING
            RepositoryCRUD.update_status(
                db,
                repository,
                RepositoryStatus.CLONING,
            )

            # Step 2 - Clone repository
            self.clone.clone_repository(
                repository.clone_url,
                repository.id,
            )

            # Step 3 - Update status to INDEXING
            RepositoryCRUD.update_status(
                db,
                repository,
                RepositoryStatus.INDEXING,
            )

            # Step 4 - Index repository
            await self.index.index_repository(
                repository.id,
            )

            # Step 5 - Delete temporary clone
            RepositoryManager.delete_repository(
                repository.id,
            )

            # Step 6 - Update status to READY
            RepositoryCRUD.update_status(
                db,
                repository,
                RepositoryStatus.READY,
            )

        except Exception:
            RepositoryManager.delete_repository(
                repository_id,
            )

            repository = RepositoryCRUD.get_by_id(
                db,
                repository_id,
            )

            if repository:
                RepositoryCRUD.update_status(
                    db,
                    repository,
                    RepositoryStatus.FAILED,
                )

            raise

        finally:
            db.close()
