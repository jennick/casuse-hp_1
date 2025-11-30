from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Maak de SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def _session_generator() -> Generator[Session, None, None]:
    """
    Interne generator die een database-sessie oplevert en
    netjes sluit na gebruik.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Generator[Session, None, None]:
    """
    Nieuwe naam die we in de recentere code gebruiken.
    """
    yield from _session_generator()


def get_db() -> Generator[Session, None, None]:
    """
    Oude naam die nog in bestaande endpoints/routers gebruikt wordt.
    Dit is een alias voor get_session(), zodat oude en nieuwe code
    tegelijk blijven werken.
    """
    yield from _session_generator()
