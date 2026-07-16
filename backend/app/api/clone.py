from fastapi import APIRouter

from app.services.clone_service import CloneService

router = APIRouter(
    prefix="/clone",
    tags=["Clone"],
)


@router.post("/")
async def clone_repo():

    path = CloneService.clone_repository(
        clone_url="https://github.com/react/react.git",
        repository_id=10270250,
    )

    return {
        "message": "Repository cloned successfully.",
        "path": str(path),
    }