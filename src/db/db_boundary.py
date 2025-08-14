from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator, Mapping

from sqlalchemy.exc import IntegrityError, DBAPIError

from src.services.errors import (
    ServiceError,
    Conflict,
    ValidationFailed,
    PreconditionFailed,
    ExternalServiceError,
    NotUniqueEmail
)

# по желанию: человекочитаемые тексты под конкретные ограничения
CONSTRAINT_MAP: dict[str, dict[str, str]] = {
    "user_email_key": {
        "code": "NOT_UNIQUE_EMAIL",
        "message": "Email already taken",
    },
}
CONSTRAINT_EXCEPTION: dict[str, type[ServiceError]] = {
    "user_email_key": NotUniqueEmail,
}


def _sqlstate(exc: BaseException) -> str | None:
    return getattr(getattr(exc, "orig", None), "sqlstate", None)


def _cname(exc: BaseException) -> str | None:
    orig = getattr(exc, "orig", None)
    return getattr(getattr(orig, "diag", None), "constraint_name", None) or getattr(orig, "constraint_name", None)


@asynccontextmanager
async def translate_db_errors(
        constraint_map: Mapping[str, Mapping[str, str]] | None = None,
        constraint_exp: Mapping[str, type[ServiceError]] = None,
        *,
        debug_details: bool = False,
) -> AsyncIterator[None]:
    cmap = constraint_map or CONSTRAINT_MAP
    emap = constraint_exp or CONSTRAINT_EXCEPTION
    try:
        yield
    except IntegrityError as e:
        sqlstate = _sqlstate(e)
        cname = _cname(e)
        mapped = cmap.get(cname) if cname else None
        msg = (mapped or {}).get("message")
        details = {}
        if debug_details and cname:
            details["constraint"] = cname
        if debug_details and sqlstate:
            details["sqlstate"] = sqlstate
        e_mapped = emap.get(cname) if cname else None
        if e_mapped:
            msg = (mapped or {}).get("message")
            raise e_mapped(msg, details=details) from e

        if sqlstate == "23505":  # unique_violation
            raise Conflict(msg or "Unique constraint violated", details=details) from e
        if sqlstate == "23503":  # foreign_key_violation
            raise PreconditionFailed(msg or "Foreign key violation", details=details) from e
        if sqlstate == "23502":  # not_null_violation
            raise ValidationFailed(msg or "Null value not allowed", details=details) from e
        if sqlstate == "23514":  # check_violation
            raise ValidationFailed(msg or "Check constraint violated", details=details) from e
        raise ExternalServiceError("Integrity error", details=details or {"sqlstate": sqlstate}) from e
    except DBAPIError as e:
        raise ExternalServiceError("Database error", details={"type": e.__class__.__name__}) from e
