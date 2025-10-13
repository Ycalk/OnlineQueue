import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import Self


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
    api_prefix: str = "/api/v1"

    secret_key: str | None = None

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
            if not self.secret_key:
                self.secret_key = secrets.token_urlsafe(32)
                print(f"⚠️  DEBUG MODE: Generated secret key: {self.secret_key}")

            if not self.postgres_host:
                print("⚠️  DEBUG MODE: Using in-memory SQLite database")

        return self


settings = Settings()  # type: ignore
