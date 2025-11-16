import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# 👇 SQLAlchemy exceptions
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class GlobalErrorHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            # Normal request flow
            response = await call_next(request)
            return response

        # ─────────────────────────────────────────────
        # FastAPI / HTTP errors
        # ─────────────────────────────────────────────
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )

        except RequestValidationError as exc:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST,
                content={"detail": exc.errors()},
            )

        # ─────────────────────────────────────────────
        # Database errors (SQLAlchemy)
        # ─────────────────────────────────────────────
        except IntegrityError as exc:
            # e.g. duplicate email, FK violation, etc.
            # optional: log full trace
            error_trace = traceback.format_exc()
            print("🔥 DB IntegrityError:")
            print(error_trace)

            return JSONResponse(
                status_code=HTTP_409_CONFLICT,
                content={
                    "detail": "Database integrity error (duplicate or invalid reference).",
                    "error": str(exc.orig) if getattr(exc, "orig", None) else str(exc),
                },
            )

        except SQLAlchemyError as exc:
            # any other SQLAlchemy-related error
            error_trace = traceback.format_exc()
            print("🔥 DB SQLAlchemyError:")
            print(error_trace)

            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Database error occurred.",
                    "error": str(exc),
                },
            )

        # ─────────────────────────────────────────────
        # Catch-all for any other unhandled exception
        # ─────────────────────────────────────────────
        except Exception as exc:
            error_trace = traceback.format_exc()
            print("🔥 Global Error Handler:")
            print(error_trace)

            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "error": str(exc),  # remove in prod if sensitive
                },
            )
