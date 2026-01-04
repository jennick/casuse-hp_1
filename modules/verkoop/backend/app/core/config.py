import os
from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuratie voor de verkoop-backend.
    Alles kan overschreven worden via environment variabelen (.env / docker).
    """

    # -------------------------------
    # Algemene app config
    # -------------------------------
    APP_NAME: str = "Casuse Verkoopmodule"
    PROJECT_NAME: str = "Casuse Verkoopmodule"
    API_V1_STR: str = "/api/v1"

    # -------------------------------
    # Database configuratie
    # -------------------------------
    # Voorbeeld:
    # DATABASE_URL=postgresql+psycopg://verkoop:verkoop@verkoop-db:5432/verkoop
    DATABASE_URL: str

    # -------------------------------
    # CORS configuratie
    # -------------------------------
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
            return [i.strip() for i in v.split(",") if i.strip()]

        if isinstance(v, (list, tuple)):
            return list(v)

        raise ValueError("BACKEND_CORS_ORIGINS heeft een ongeldig formaat")

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Output voor CORSMiddleware → altijd strings.
        """
        if not self.BACKEND_CORS_ORIGINS:
            return ["*"]

        return [str(origin) for origin in self.BACKEND_CORS_ORIGINS]

    # -------------------------------------------------------
    # Website API (interne sync logica)
    # -------------------------------------------------------
    # → verkoop-backend zal klanten ophalen van website-backend
    WEBSITE_API_BASE_URL: str = "http://website-backend:20052"

    # Interne beveiliging
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "casuse-internal-2025")

    # Optioneel: indien later nodig voor admin-login naar website
    WEBSITE_ADMIN_EMAIL: str | None = None
    WEBSITE_ADMIN_PASSWORD: str | None = None

    # -------------------------------
    # Logging
    # -------------------------------
    LOG_LEVEL: str = "INFO"

    # -------------------------------
    # Pydantic settings
    # -------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Enkel één keer laden, performance optimalisatie.
    """
    return Settings()


settings = get_settings()
