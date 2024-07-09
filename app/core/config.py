import os
from enum import Enum
from typing import Any
from datetime import datetime

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModeEnum(str, Enum):
    DEV = "development"
    TEST = "testing"
    PROD = "production"


class Settings(BaseSettings):
    MODE: ModeEnum = ModeEnum.DEV
    PROJECT_NAME: str = "exampleproject-api"

    # in practice GIT_SHA will be populated by github action via docker build arg
    GIT_SHA: str = "dev"
    BUILD_INFO: str = ""

    # return some build information about the app
    # for status checking purposes
    @field_validator("BUILD_INFO", mode="after")
    def assemble_build_info(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                _ts = datetime.now().isoformat(timespec="seconds")
                _build_ts = os.path.abspath("build_ts")
                if os.path.exists(_build_ts):
                    _ts = open(_build_ts).read().strip()
                return f"git_sha:{info.data['GIT_SHA'][:8]} build_ts:{_ts}"
        return v

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    ASYNC_POSTGRES_URI: PostgresDsn | str = ""

    @field_validator("ASYNC_POSTGRES_URI", mode="after")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                return PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=info.data["DATABASE_USER"],
                    password=info.data["DATABASE_PASSWORD"],
                    host=info.data["DATABASE_HOST"],
                    port=info.data["DATABASE_PORT"],
                    path=info.data["DATABASE_NAME"],
                )
        return v

    ASYNC_SQLITE_URI: str = ""

    @field_validator("ASYNC_SQLITE_URI", mode="after")
    def assemble_sqlite_uri(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                return f"sqlite+aiosqlite:///{info.data['PROJECT_NAME']}.db"
        return v

    DATABASE_ENGINE: str = "postgres"

    AUTHENTICATION_ENABLED: bool = True 
    AUTH_JWT_SECRET: str

    _env_file = os.path.abspath(".env")
    model_config = SettingsConfigDict(case_sensitive=True, env_file=_env_file)


settings = Settings()
