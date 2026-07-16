from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeAtlas AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()