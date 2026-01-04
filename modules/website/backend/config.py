import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # ============================================================
    # DATABASE CONFIG
    # ============================================================
    WEBSITE_DB_HOST: str = os.getenv("WEBSITE_DB_HOST", "website-db")
    WEBSITE_DB_PORT: str = os.getenv("WEBSITE_DB_PORT", "5432")
    WEBSITE_DB_NAME: str = os.getenv("WEBSITE_DB_NAME", "casuse_hp_website")
    WEBSITE_DB_USER: str = os.getenv("WEBSITE_DB_USER", "website_user")
    WEBSITE_DB_PASSWORD: str = os.getenv("WEBSITE_DB_PASSWORD", "website_password")

    # ============================================================
    # BACKEND / AUTH
    # ============================================================
    WEBSITE_BACKEND_PORT: int = int(os.getenv("WEBSITE_BACKEND_PORT", "8000"))

    WEBSITE_JWT_SECRET: str = os.getenv(
        "WEBSITE_JWT_SECRET",
        "CHANGE_ME_LOCAL_ONLY",
    )
    WEBSITE_JWT_ALGORITHM: str = os.getenv(
        "WEBSITE_JWT_ALGORITHM",
        "HS256",
    )
    WEBSITE_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("WEBSITE_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # ============================================================
    # REGISTRATION / PASSWORD SETUP TOKENS
    # ============================================================
    # ❗ Wordt gebruikt in services/registration_tokens.py
    REGISTRATION_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("REGISTRATION_TOKEN_EXPIRE_MINUTES", "60")
    )

    # Bestaande waarde behouden (backwards compatibility)
    WEBSITE_REGISTRATION_TOKEN_TTL_MINUTES: int = int(
        os.getenv("WEBSITE_REGISTRATION_TOKEN_TTL_MINUTES", "60")
    )

    # ============================================================
    # EMAIL / SMTP (MailHog / productie)
    # ============================================================
    WEBSITE_EMAIL_ENABLED: bool = os.getenv(
        "WEBSITE_EMAIL_ENABLED",
        "false",
    ).lower() == "true"

    WEBSITE_SMTP_HOST: str = os.getenv("WEBSITE_SMTP_HOST", "localhost")
    WEBSITE_SMTP_PORT: int = int(os.getenv("WEBSITE_SMTP_PORT", "1025"))
    WEBSITE_SMTP_TLS: bool = os.getenv(
        "WEBSITE_SMTP_TLS",
        "false",
    ).lower() == "true"

    WEBSITE_SMTP_USERNAME: str = os.getenv("WEBSITE_SMTP_USERNAME", "")
    WEBSITE_SMTP_PASSWORD: str = os.getenv("WEBSITE_SMTP_PASSWORD", "")
    WEBSITE_EMAIL_FROM: str = os.getenv(
        "WEBSITE_EMAIL_FROM",
        "no-reply@casuse.mx",
    )

    # ============================================================
    # INTERNAL SERVICE AUTH (microservice → microservice)
    # ============================================================
    INTERNAL_API_KEY: str = os.getenv(
        "INTERNAL_API_KEY",
        "casuse-internal-2025",
    )

    # ============================================================
    # ENV / URLS
    # ============================================================
    WEBSITE_ENV: str = os.getenv("WEBSITE_ENV", "local")

    # ❌ NIET gebruiken voor klant-links
    # (blijft bestaan voor interne/admin context)
    WEBSITE_PUBLIC_BASE_URL: str = os.getenv(
        "WEBSITE_PUBLIC_BASE_URL",
        "http://localhost:20190",
    )

    # ✅ WEL gebruiken voor klanten (e-mails, password setup, login)
    PUBLIC_APP_BASE_URL: str = os.getenv(
        "PUBLIC_APP_BASE_URL",
        "http://localhost:3000",  # website-app / klantportaal
    )

    # ============================================================
    # CORS
    # ============================================================
    WEBSITE_CORS_ORIGINS: str = os.getenv(
        "WEBSITE_CORS_ORIGINS",
        "http://localhost:20060,http://localhost:20190",
    )

    # ============================================================
    # SQLALCHEMY
    # ============================================================
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.WEBSITE_DB_USER}:"
            f"{self.WEBSITE_DB_PASSWORD}@"
            f"{self.WEBSITE_DB_HOST}:{self.WEBSITE_DB_PORT}/"
            f"{self.WEBSITE_DB_NAME}"
        )


# Singleton
settings = Settings()
