
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
import os

class Base(DeclarativeBase):
    pass

_engine = None
SessionLocal = None

def get_engine():
    global _engine, SessionLocal
    if _engine is None:
        url = os.getenv("DATABASE_URL")
        _engine = create_engine(url, pool_pre_ping=True)
        SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine

def get_session():
    if SessionLocal is None:
        get_engine()
    return SessionLocal()
