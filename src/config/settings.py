import os

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int = os.environ.get("DB_PORT", "5432")
    DB_USER: str = os.environ.get("DB_USER", "banner")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "banner")
    DB_NAME: str = os.environ.get("DB_NAME", "banner")
    DB_URL: str = os.environ.get(
        "DB_URL",
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
    DEBUG: bool = os.environ.get("DEBUG", True)
    APP_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")
    APP_PORT: int = os.environ.get("APP_PORT", 8000)
    UVICORN_WORKERS: int = os.environ.get("UVICORN_WORKERS", 1)

    JWT_SECRET_KEY: str = os.environ.get(
        "JWT_SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    )
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")


settings = Settings()
