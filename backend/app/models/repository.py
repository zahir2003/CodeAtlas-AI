from datetime import datetime
from uuid import uuid4
import enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RepositoryStatus(str, enum.Enum):
    PENDING = "pending"
    CLONING = "cloning"
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    github_url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    canonical_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    redirected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    repository_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    owner: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    stars: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    forks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    visibility: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    clone_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    default_branch: Mapped[str] = mapped_column(
        String(100),
        default="main",
        nullable=False,
    )

    latest_commit: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[RepositoryStatus] = mapped_column(
        Enum(RepositoryStatus),
        default=RepositoryStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="repository",
        cascade="all, delete-orphan",
    )
