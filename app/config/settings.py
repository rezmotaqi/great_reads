from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_ignore_empty=True)

    PROJECT_NAME: str
    PROJECT_DESCRIPTION: Optional[str] = "A site for managing the process of reading books."

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str
    MONGO_PASSWORD: Optional[str] = None
    MONGO_USER: Optional[str] = None

    VERSION: str = '1.0.0'
    API_ROUTE_PREFIX: str = '/api'


settings = Settings()
