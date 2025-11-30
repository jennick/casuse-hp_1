from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Applicatieconfiguratie voor de verkoop-backend.

    - Alle waarden zijn overridebaar via environment variabelen.
    - In docker-compose wordt normaliter een `.env` ingeladen.
    """

    # Algemene app-configuratie
    APP_NAME: str = "Casuse Verkoopmodule"
    PROJECT_NAME: str = "Casuse Verkoopmodule"  # backward compat
    API_V1_STR: str = "/api/v1"

    # Database connectiestring, bv.
    # postgresql+psycopg://verkoop:verkoop@verkoop-db:5432/verkoop
    DATABASE_URL: str

    # ---------------- CORS-instellingen ----------------
    # Kan in .env gezet worden als:
    # BACKEND_CORS_ORIGINS=["http://localhost:20040","http://localhost:5173"]
    # of als komma-gescheiden string:
    # BACKEND_CORS_ORIGINS=http://localhost:20040,http://localhost:5173
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        """
        Ondersteunt:
        - lege waarde
        - lijst ["http://...", "http://..."]
        - string "http://...,http://..."
        """
        if not v:
            return []

        if isinstance(v, str):
            # komma-gescheiden string => lijst
            return [i.strip() for i in v.split(",") if i.strip()]

        if isinstance(v, (list, tuple)):
            return list(v)

        raise ValueError("BACKEND_CORS_ORIGINS heeft een ongeldig formaat")

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Interface die in app/main.py gebruikt wordt bij CORSMiddleware:

            allow_origins = settings.cors_origins_list
        """
        if not self.BACKEND_CORS_ORIGINS:
            # default: alles toelaten (kan je strenger maken in productie)
            return ["*"]

        return [str(origin) for origin in self.BACKEND_CORS_ORIGINS]

    # --------------- Website-API (customer-sync) ---------------
    # Wordt gebruikt door app/api/v1/customers_sync.py
    WEBSITE_API_BASE_URL: str = "http://host.docker.internal:20052"
    WEBSITE_ADMIN_EMAIL: str | None = None
    WEBSITE_ADMIN_PASSWORD: str | None = None

    # --------------- Logging ---------------
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


@lru_cache()
def get_settings() -> Settings:
    """Gecachte instantie zodat settings maar één keer geparset wordt."""
    return Settings()


settings = get_settings()
