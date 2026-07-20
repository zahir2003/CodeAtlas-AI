from fastapi import FastAPI

from app.core.config import settings
from app.api.health import router as health_router
from app.api.repositories import router as repository_router
from app.core.logging_config import setup_logging
from app.storage.repository_manager import RepositoryManager
from app.api.clone import router as clone_router
from app.api.discovery import router as discovery_router
from app.api.jobs import router as jobs_router
from app.api.parser import router as parser_router
from app.api.routes.indexing import router as indexing_router
from app.api.routes.chat import router as chat_router
from app.api.routes.search import router as search_router
from app.clients.qdrant_client import QdrantService

# from app.parsers.ast_parser import ASTParser

setup_logging()

qdrant = QdrantService()

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

app.include_router(
    parser_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    indexing_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    search_router,
    prefix=settings.API_PREFIX,
)

app.include_router(chat_router)

# app.include_router(chat_router)


@app.on_event("startup")
async def startup():

    RepositoryManager.initialize()

    await qdrant.initialize()


@app.get("/", tags=["Home"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}"
    }
