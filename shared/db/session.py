# backend/shared/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.utils.config import settings

# Create the global engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,   # set True if you want to see SQL logs
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
