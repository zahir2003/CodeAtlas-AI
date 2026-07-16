from fastapi import FastAPI

from app.core.config import settings
from app.api.health import router as health_router
from app.api.repositories import router as repository_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(health_router)

app.include_router(
    repository_router,
    prefix=settings.API_PREFIX
)


@app.get("/", tags=["Home"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}"
    }