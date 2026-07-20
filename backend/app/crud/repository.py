from uuid import UUID

from sqlalchemy.orm import Session

from app.models.repository import Repository, RepositoryStatus


class RepositoryCRUD:
    """Database operations for Repository."""

    @staticmethod
    def create(
        db: Session,
        repository: Repository,
    ) -> Repository:
        db.add(repository)
        db.commit()
        db.refresh(repository)
        return repository

    @staticmethod
    def get_by_id(
        db: Session,
        repository_id: UUID,
    ) -> Repository | None:
        return db.query(Repository).filter(Repository.id == repository_id).first()

    @staticmethod
    def get_by_github_url(
        db: Session,
        github_url: str,
    ) -> Repository | None:
        return db.query(Repository).filter(Repository.github_url == github_url).first()

    @staticmethod
    def list_all(
        db: Session,
    ) -> list[Repository]:
        return db.query(Repository).order_by(Repository.created_at.desc()).all()

    @staticmethod
    def update_status(
        db: Session,
        repository: Repository,
        status: RepositoryStatus,
    ) -> Repository:
        repository.status = status
        db.commit()
        db.refresh(repository)
        return repository

    @staticmethod
    def delete(
        db: Session,
        repository: Repository,
    ) -> None:
        db.delete(repository)
        db.commit()
