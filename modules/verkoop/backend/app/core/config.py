
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "casuse-verkoop"
    ENV: str = "dev"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_AUDIENCE: str = "casuse-hp"
    ACCESS_TOKEN_ISSUER: str = "casuse-hp"
    JWT_PUBLIC_KEY: str = "changeme"
    JWT_ALGO: str = "RS256"

    DATABASE_URL: str
    WEBSITE_DB_URL: str | None = None

    CORS_ALLOW_ORIGINS: str = "http://localhost:20040"

    AI_ADVISOR_ENABLED: bool = True
    AUTO_ASSIGN_ENABLED: bool = True

    PAYMENTS_PROVIDER: str = "stripe"
    PAYMENTS_WEBHOOK_SECRET: str = "changeme"

    RATE_LIMIT_PER_MIN: int = 120
    IDEMPOTENCY_TTL_SECONDS: int = 3600

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
