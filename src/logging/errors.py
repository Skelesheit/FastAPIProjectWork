import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from src.services.errors import ServiceError

log = logging.getLogger("app")

from .context import common_extra

def log_service_error(request: Request, exc: ServiceError) -> None:
    log.error(f"ServiceError: {exc.code} {exc.message}",
              exc_info=exc,
              **common_extra(request, code=exc.code, status=exc.status_code, details=exc.details))

def log_validation_error(request: Request, exc: RequestValidationError) -> None:
    details = {"errors": [{"loc": e["loc"], "msg": e["msg"], "type": e["type"]} for e in exc.errors()]}
    log.warning("Validation failed", **common_extra(request, code="VALIDATION_FAILED", status=422, details=details))

def log_http_exception(request: Request, exc: StarletteHTTPException) -> None:
    log.warning(f"HTTPException: {exc.status_code} {exc.detail}",
                **common_extra(request, code=f"HTTP_{exc.status_code}", status=exc.status_code))

def log_integrity_error(request: Request, exc: IntegrityError) -> None:
    log.error("DB constraint violation", exc_info=exc,
              **common_extra(request, code="DB_CONSTRAINT_VIOLATION", status=409))

def log_unhandled(request: Request, exc: Exception) -> None:
    log.exception("Unhandled exception", **common_extra(request, code="INTERNAL_ERROR", status=500))
