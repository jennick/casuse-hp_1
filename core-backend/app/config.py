from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "casuse-hp-core"
    APP_PORT: int = 20010
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql+psycopg://casuse_hp:casuse_hp@core-db:5432/casuse_hp"
    JWT_SECRET: str = "CHANGE_ME_IN_PROD"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200
    CORS_ALLOWED_ORIGINS: str = "http://localhost:20020"
    ENABLE_2FA: bool = False
    AI_PROVIDER: str = "mock"

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings() -> "Settings":
    return Settings()
