from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

BACKEND_DIR = PROJECT_ROOT / "backend"

APP_DIR = BACKEND_DIR / "app"

LOGS_DIR = PROJECT_ROOT / "logs"

STORAGE_DIR = PROJECT_ROOT / "storage"

REPOSITORIES_DIR = STORAGE_DIR / "repositories"

CACHE_DIR = STORAGE_DIR / "cache"

EMBEDDINGS_DIR = STORAGE_DIR / "embeddings"

TEMP_DIR = STORAGE_DIR / "temp"


class Settings(BaseSettings):
    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    PROJECT_NAME: str = "CodeAtlas AI"

    VERSION: str = "1.0.0"

    API_PREFIX: str = "/api/v1"

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    SECRET_KEY: str = ""

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --------------------------------------------------
    # GitHub
    # --------------------------------------------------

    GITHUB_TOKEN: str = ""

    # --------------------------------------------------
    # NVIDIA Build
    # --------------------------------------------------

    NVIDIA_API_KEY: str = ""

    EMBEDDING_MODEL: str = "nvidia/nv-embedcode-7b-v1"

    CHAT_MODEL: str = "z-ai/glm-5.2"

    # --------------------------------------------------
    # Supabase
    # --------------------------------------------------

    SUPABASE_URL: str = ""

    SUPABASE_ANON_KEY: str = ""

    SUPABASE_SERVICE_ROLE_KEY: str = ""

    DATABASE_URL: str = ""

    # --------------------------------------------------
    # Qdrant
    # --------------------------------------------------

    QDRANT_URL: str = ""

    QDRANT_API_KEY: str = ""

    QDRANT_COLLECTION: str = "codeatlas_chunks"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )


settings = Settings()


# --------------------------------------------------
# Create required directories automatically
# --------------------------------------------------

for directory in (
    LOGS_DIR,
    STORAGE_DIR,
    REPOSITORIES_DIR,
    CACHE_DIR,
    EMBEDDINGS_DIR,
    TEMP_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )
