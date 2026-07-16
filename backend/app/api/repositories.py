from fastapi import APIRouter

from app.schemas.repository import RepositoryCreate
from app.services.repository_service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"]
)


@router.post("/")
async def create_repository(repository: RepositoryCreate):

    return RepositoryService.create_repository(repository)