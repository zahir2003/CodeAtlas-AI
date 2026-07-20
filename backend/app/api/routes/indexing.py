from uuid import UUID

from fastapi import APIRouter

from app.services.indexing_service import IndexingService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)

service = IndexingService()


@router.post("/{repository_id}/index")
async def index_repository(
    repository_id: UUID,
):
    return await service.index_repository(repository_id)
