from fastapi import APIRouter

from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.repository_service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"]
)


@router.post(
    "/",
    response_model=RepositoryResponse
)
async def create_repository(repository: RepositoryCreate):

    return await RepositoryService.create_repository(repository)