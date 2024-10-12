from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_ignore_empty=True
    )

    PROJECT_NAME: str = "Great reads"
    PROJECT_DESCRIPTION: Optional[str] = "Exercising OOP and design patterns."

    ALGORITHM: str = "HS256"

    MONGO_HOST: str = "mongodb://localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "great_reads"
    MONGO_PASSWORD: Optional[str] = None
    MONGO_USER: Optional[str] = None

    REDIS_URL: str = "redis://localhost:6379"

    VERSION: str = "1.0.0"
    API_ROUTE_PREFIX: str = "/api"
    SECRET_KEY: str = "123"


settings = Settings()
