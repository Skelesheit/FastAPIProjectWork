from typing import Any, Mapping, Optional


class ServiceError(Exception):
    status_code: int = 500
    code: str = "INTERNAL_ERROR"
    message: str = "Internal server error"
    details: Optional[Mapping[str, Any]] = None
    headers: Optional[Mapping[str, str]] = None  # для 401 ошибок

    def __init__(
            self,
            message: str | None = None,
            *,
            details: Mapping[str, Any] | None = None,
            headers: Mapping[str, str] | None = None
    ):
        if message is not None:
            self.message = message
        if details is not None:
            self.details = details
        if headers is not None:
            self.headers = headers

    def to_body(self) -> dict[str, Any]:
        return {
            "error":
                {
                    "code": self.code,
                    "message": self.message,
                    "details": dict(self.details or {})
                }
        }


# === Общие доменные ===
class NotFound(ServiceError):
    status_code = 404
    code = "NOT_FOUND"


class Conflict(ServiceError):
    status_code = 409
    code = "CONFLICT"


class ValidationFailed(ServiceError):
    status_code = 422
    code = "VALIDATION_FAILED"


class BadRequest(ServiceError):
    status_code = 400
    code = "BAD_REQUEST"
    message = "Bad request"


class CaptchaNotVerified(ServiceError):
    status_code = 422
    code = "CAPTCHA_NOT_VERIFIED"
    message = "captcha not verified"


class NotUniqueEmail(ServiceError):
    status_code = 409
    code = "NOT_UNIQUE_EMAIL"
    message = "not unique email"


class PreconditionFailed(ServiceError):
    status_code = 412
    code = "PRECONDITION_FAILED"


class Forbidden(ServiceError):
    status_code = 403
    code = "FORBIDDEN"


class UnknownUserType(ValidationFailed):
    code = "UNKNOWN_USER_TYPE"
    message = "Неизвестный тип пользователя"


class RateLimited(ServiceError):
    status_code = 429
    code = "RATE_LIMITED"


class ExternalServiceError(ServiceError):
    status_code = 502
    code = "UPSTREAM_ERROR"


# === Клиенты / ИНН ===
class INNValidationError(ValidationFailed):
    """Базовая ошибка валидации ИНН"""
    code = "INN_VALIDATION_ERROR"
    message = "Invalid INN format"


class INNMissing(INNValidationError):
    code = "INN_MISSING"
    message = "ИНН не может быть пустым"


class INNInvalidFormat(INNValidationError):
    code = "INN_INVALID_FORMAT"
    message = "ИНН должен состоять из цифр"


class INNInvalidLength(INNValidationError):
    code = "INN_INVALID_LENGTH"
    message = "ИНН должен иметь длину 10 или 12 цифр"


# === Аутентификация / Авторизация ===
class Unauthorized(ServiceError):
    status_code = 401
    code = "UNAUTHORIZED"
    message = "Unauthorized"


# === Клиенты / Верификация ===

class EmailVerificationError(ServiceError):
    """Базовая ошибка верификации email"""
    status_code = 400
    code = "EMAIL_VERIFICATION_ERROR"
    message = "Email verification failed"


class EmailVerificationTokenInvalid(EmailVerificationError):
    status_code = 401  # Unauthorized для невалидного токена
    code = "EMAIL_VERIFICATION_TOKEN_INVALID"
    message = "Invalid email verification token"


class UserNotVerified(ServiceError):
    status_code = 403  # Forbidden - доступ запрещен пока не верифицирован
    code = "USER_NOT_VERIFIED"
    message = "User email is not verified"


class InvalidEntityType(Forbidden):
    code = "INVALID_ENTITY_TYPE"
    message = "Only legal entities and individual entrepreneurs can invite members"


class JoinTokenError(ServiceError):
    """Базовая ошибка для присоединения по токену"""
    status_code = 400
    code = "JOIN_TOKEN_ERROR"
    message = "Join token error"


class EnterpriseNotFound(NotFound):
    code = "ENTERPRISE_NOT_FOUND"
    message = "Enterprise not found"


class JoinTokenInvalid(JoinTokenError):
    status_code = 401  # Unauthorized для невалидного токена
    code = "JOIN_TOKEN_INVALID"
    message = "Invalid join token"


class EmailVerificationFailed(EmailVerificationError):
    code = "EMAIL_VERIFICATION_FAILED"
    message = "Failed to verify email"


class JoinEmployeeError(ServiceError):
    """Базовая ошибка для присоединения сотрудника"""
    status_code = 400
    code = "JOIN_EMPLOYEE_ERROR"
    message = "Failed to join employee"


class UserNotRegistered(NotFound):
    code = "USER_NOT_REGISTERED"
    message = "Пользователь ещё не зарегистрирован"


class UserAlreadyInEnterprise(Conflict):
    code = "USER_ALREADY_IN_ENTERPRISE"
    message = "Пользователь уже принадлежит компании"


# токены доступа
class AccessTokenMissing(Unauthorized):
    code = "ACCESS_TOKEN_MISSING"
    message = "Access token is missing"


class AccessTokenMalformed(Unauthorized):
    code = "ACCESS_TOKEN_MALFORMED"
    message = "Access token is malformed"


class AccessTokenInvalid(Unauthorized):
    code = "ACCESS_TOKEN_INVALID"
    message = "Access token is invalid"


class AccessTokenExpired(Unauthorized):
    code = "ACCESS_TOKEN_EXPIRED"
    message = "Access token has expired"


# refresh токены / сессии
class RefreshTokenMissing(Unauthorized):
    code = "REFRESH_TOKEN_MISSING"
    message = "Refresh token is missing"


class RefreshTokenInvalid(Unauthorized):
    code = "REFRESH_TOKEN_INVALID"
    message = "Refresh token is invalid"


class RefreshTokenExpired(Unauthorized):
    code = "REFRESH_TOKEN_EXPIRED"
    message = "Refresh token has expired"


class RefreshTokenRevoked(Unauthorized):
    code = "REFRESH_TOKEN_REVOKED"
    message = "Refresh token has been revoked"


class SessionNotFound(Unauthorized):
    code = "SESSION_NOT_FOUND"
    message = "Session not found"


# учётка/права
class InvalidCredentials(Unauthorized):
    code = "INVALID_CREDENTIALS"
    message = "Invalid login or password"


class UserDisabled(Forbidden):
    code = "USER_DISABLED"
    message = "User account is disabled"


class EmailNotConfirmed(Forbidden):
    code = "EMAIL_NOT_CONFIRMED"
    message = "Email is not confirmed"


class TwoFARequired(Unauthorized):
    code = "TWO_FA_REQUIRED"
    message = "Two-factor authentication required"


class TwoFAInvalid(Unauthorized):
    code = "TWO_FA_INVALID"
    message = "Invalid two-factor code"


class CSRFTokenMissing(Forbidden):
    code = "CSRF_TOKEN_MISSING"
    message = "CSRF token is missing"


class CSRFTokenInvalid(Forbidden):
    code = "CSRF_TOKEN_INVALID"
    message = "CSRF token is invalid"


class InsufficientScope(Forbidden):
    code = "INSUFFICIENT_SCOPE"
    message = "Insufficient scope"


# enterprise / владение ресурсами
class EnterpriseRequired(Forbidden):
    code = "ENTERPRISE_REQUIRED"
    message = "Enterprise context required"


class EnterpriseMismatch(Forbidden):
    code = "ENTERPRISE_MISMATCH"
    message = "Resource belongs to another enterprise"


# приглашения/подтверждения (из твоих эндпоинтов)
class InviteTokenInvalid(Unauthorized):
    code = "INVITE_TOKEN_INVALID"
    message = "Invite token is invalid"


class InviteTokenExpired(Unauthorized):
    code = "INVITE_TOKEN_EXPIRED"
    message = "Invite token has expired"


class InviteTokenRevoked(Unauthorized):
    code = "INVITE_TOKEN_REVOKED"
    message = "Invite token has been revoked"


class EmailConfirmTokenInvalid(Unauthorized):
    code = "EMAIL_CONFIRM_TOKEN_INVALID"
    message = "Email confirmation token is invalid"


class EmailConfirmTokenExpired(Unauthorized):
    code = "EMAIL_CONFIRM_TOKEN_EXPIRED"
    message = "Email confirmation token has expired"


# если у тебя уже есть базовые Forbidden/BadRequest — используй их
class InviteByInnNotAllowedForIndividuals(Forbidden):
    code = "INVITE_BY_INN_NOT_ALLOWED"
    message = "Только ИП или юридическое лицо могут отправлять приглашения по ИНН."


class InnRequiredForInvitation(BadRequest):
    code = "INN_REQUIRED"
    message = "Для отправки приглашения по ИНН необходимо указать ИНН организации."


class JoinTokenExpired(Unauthorized):
    code = "JOIN_TOKEN_EXPIRED"
    message = "Join token has expired"
