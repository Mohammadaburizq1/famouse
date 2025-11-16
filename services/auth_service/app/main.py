from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.auth_service.app.api.v1.endpoints import auth, users
from services.auth_service.app.middleware.error_handler import GlobalErrorHandlerMiddleware

from .core.config import settings          # ✅ relative import
from .models import Base                   # ✅ relative import (models/__init__.py)
from shared.db.database import engine      # ✅ shared package


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DEV ONLY: create tables on startup
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")
    yield
    print("Application shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(GlobalErrorHandlerMiddleware)

    # include routers from auth.py and users.py
    app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
    app.include_router(users.router, prefix=settings.API_V1_PREFIX)

    @app.get(f"{settings.API_V1_PREFIX}/health")
    def health():
        return {"status": "ok", "service": "auth"}

    return app


app = create_app()
