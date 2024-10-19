from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_ignore_empty=True
    )

    PROJECT_NAME: str = "Great reads"
    PROJECT_DESCRIPTION: str | None = "Exercising OOP and design patterns."

    ALGORITHM: str = "HS256"

    MONGO_HOST: str = "mongodb://localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "great_reads"
    MONGO_PASSWORD: str | None = None
    MONGO_USER: str | None = None

    REDIS_URL: str = "redis://localhost:6379"

    VERSION: str = "1.0.0"
    API_ROUTE_PREFIX: str = "/api"
    SECRET_KEY: str = "123"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000
    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str


settings = Settings()
