from fastapi import APIRouter

from app.discovery.file_discovery import FileDiscovery
from app.storage.repository_manager import RepositoryManager
from uuid import UUID

router = APIRouter(
    prefix="/discovery",
    tags=["Discovery"],
)


@router.get("/{repository_id}")
async def discover(repository_id: UUID):

    path = RepositoryManager.get_repository_path(repository_id)

    manifest = FileDiscovery.discover(path)

    return manifest
