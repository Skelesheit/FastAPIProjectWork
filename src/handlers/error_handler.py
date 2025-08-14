# src/handlers/error_handlers.py
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.logging.errors import (
    log_service_error,
    log_validation_error,
    log_http_exception,
    log_integrity_error,
    log_unhandled,
)
from src.services.errors import ServiceError, ValidationFailed, Conflict


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def handle_service_error(request: Request, exc: ServiceError):
        log_service_error(request, exc)  # ⬅️ лог
        rid = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        body = exc.to_body()
        body["request_id"] = rid
        headers = dict(getattr(exc, "headers", {}) or {})
        if exc.status_code == 401 and "WWW-Authenticate" not in headers:
            headers["WWW-Authenticate"] = "Bearer"
        return JSONResponse(status_code=exc.status_code, content=body, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        log_validation_error(request, exc)  # ⬅️ лог
        rid = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        err = ValidationFailed(details={"errors": exc.errors()})
        body = err.to_body()
        body["request_id"] = rid
        return JSONResponse(status_code=err.status_code, content=body)

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        log_http_exception(request, exc)  # ⬅️ лог
        rid = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        body = {
            "error":
                {
                    "code": f"HTTP_{exc.status_code}",
                    "message": str(exc.detail),
                    "details": {}
                },
            "request_id": rid
        }
        headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else {}
        return JSONResponse(status_code=exc.status_code, content=body, headers=headers)

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError):
        log_integrity_error(request, exc)  # ⬅️ лог
        rid = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        err = Conflict(message="Database constraint violation")
        body = err.to_body()
        body["request_id"] = rid
        return JSONResponse(status_code=err.status_code, content=body)

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception):
        log_unhandled(request, exc)  # ⬅️ лог
        rid = getattr(request.state, "request_id", None) or str(uuid.uuid4())
        body = {
            "error":
                {
                    "code": "INTERNAL_ERROR",
                    "message": "Internal server error",
                    "details": {}
                },
            "request_id": rid
        }
        return JSONResponse(status_code=500, content=body)
