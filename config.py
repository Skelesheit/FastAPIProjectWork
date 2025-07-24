import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # FastAPI
    BACKEND_HOST: str
    BACKEND_PORT: int
    BACKEND_DEBUG: bool

    # JWT
    SECRET_KEY: str
    EXPIRES_ACCESS_TOKEN_MINUTES: int
    EXPIRES_REFRESH_TOKEN_DAYS: int

    # Database
    DB_USER: str
    DB_PROVIDER: str
    DB_DRIVER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_URL: str

    # Mail
    MAIL_SECRET: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_START_TLS: bool
    MAIL_USE_TLS: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    # Base
    BASE_URL: str

    # Frontend
    FRONTEND_URL: str

    # Yandex captcha
    YANDEX_URL_VERIFY: str
    YANDEX_CAPTCHA_SECRET: str

    # Dadata
    DADATA_TOKEN: str
    DADATA_API_URL: str

    # Redis
    REDIS_PORT: int
    REDIS_PASSWORD: str

    # База данных
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    @property
    def db_orm_url(self) -> str:
        return (
            f"{self.DB_PROVIDER}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
