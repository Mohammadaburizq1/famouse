# shared/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.orm import Session

from shared.utils.config import settings

# Read URL from .env via shared.utils.config.Settings
DATABASE_URL = settings.DATABASE_URL

# Create a normal (sync) SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,   # set True if you want to see SQL in the console
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a DB session and
    closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
