from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository_service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "/",
    response_model=RepositoryResponse,
)
async def create_repository(
    repository: RepositoryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = RepositoryService()

    response = await service.create_repository(
        db=db,
        repository=repository,
    )

    background_tasks.add_task(
        service.process_repository,
        response.repository_id,
    )

    return response
