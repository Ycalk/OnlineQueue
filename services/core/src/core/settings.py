import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator, field_validator
from typing import Self, Final


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    debug: bool = False

    postgres_host: str | None = None
    postgres_port: int | None = None
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    pool_size: int = 10
    max_overflow: int = 20

    app_name: str = "Queue Management System"
    api_prefix: str = "/api"
    api_port: int = 8080

    @property
    def methods_prefix(self) -> str:
        return f"{self.api_prefix}/v1"

    secret_key: str | None = None
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    encoding_algorithm: str = "HS256"
    refresh_token_cookie_name: str = "refresh_token"
    allow_origin_regex: str = r"^(http://localhost(:\d+)?|http://127\.0\.0\.1(:\d+)?)$"

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_login: str = "guest"
    rabbitmq_password: str = "guest"

    notifications_bot_username: str
    aessiv_hex_key: str

    @model_validator(mode="after")
    def validate_production_requirements(self) -> Self:
        if not self.debug:
            missing = []
            if not self.postgres_host:
                missing.append("POSTGRES_HOST")
            if not self.postgres_port:
                missing.append("POSTGRES_PORT")
            if not self.postgres_db:
                missing.append("POSTGRES_DB")
            if not self.postgres_user:
                missing.append("POSTGRES_USER")
            if not self.postgres_password:
                missing.append("POSTGRES_PASSWORD")
            if not self.secret_key:
                missing.append("SECRET_KEY")

            if missing:
                raise ValueError(
                    f"In production mode (DEBUG=false), the following "
                    f"environment variables are required: {', '.join(missing)}"
                )

        else:
            print("⚠️  DEBUG MODE: Using in-memory SQLite database")

        return self

    @field_validator("secret_key", mode="before")
    @classmethod
    def generate_secret_key_in_debug(cls, value: str | None, info) -> str:
        if value is not None:
            return value

        if info.data.get("debug", False):
            generated = secrets.token_urlsafe(32)
            print(f"⚠️  DEBUG MODE: Generated secret key: {generated}")
            return generated

        raise ValueError("SECRET_KEY is required in production mode")


settings: Final[Settings] = Settings()  # type: ignore
