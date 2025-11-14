from __future__ import annotations
# --- Path guard so 'app' resolves when Alembic runs ---
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# Also add /app as fallback when running in container
if "/app" not in sys.path:
    sys.path.insert(0, "/app")
# ------------------------------------------------------

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.session import Base, get_engine
from app.models import *  # noqa

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
