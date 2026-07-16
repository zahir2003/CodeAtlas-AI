from fastapi import FastAPI

from app.core.config import settings
from app.api.health import router as health_router
from app.api.repositories import router as repository_router
from app.core.logging_config import setup_logging
from app.storage.repository_manager import RepositoryManager
from app.api.clone import router as clone_router
from app.api.discovery import router as discovery_router
from app.api.jobs import router as jobs_router

setup_logging()
RepositoryManager.initialize()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(health_router)

app.include_router(
    repository_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    clone_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    discovery_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    jobs_router,
    prefix=settings.API_PREFIX,
)

@app.get("/", tags=["Home"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}"
    }