from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache
from typing import Any
from pydantic import BaseModel, Field, SecretStr, PostgresDsn, model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    DotEnvSettingsSource,
    PyprojectTomlConfigSettingsSource,
)

class KeycloakSettings(BaseModel):
    model_config = SettingsConfigDict(
        env_prefix="KEYCLOAK_",
        env_nested_delimiter="_",
    )

    hostname: str = Field(default="keycloak")
    http_port: int = Field(default=8080)
    https_port: int = Field(default=8443)
    realm: str = Field(default="universal")
    http_relative_path: str = Field(default="/auth")

    @property
    def http_url(self: KeycloakSettings) -> str:
        return f"http://{self.hostname}:{self.http_port}{self.http_relative_path}"

    @property
    def https_url(self: KeycloakSettings) -> str:
        return f"https://{self.hostname}:{self.https_port}{self.http_relative_path}"

class DatabaseSettings(BaseModel):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_nested_delimiter="_",
    )

    url: PostgresDsn | None = Field(
        default=None,
        description="Full DSN, e.g. postgresql+asyncpg://user:pass@host:port/db"
    )
    hostname: str = Field(
        default="localhost",
        description="Database hostname, e.g., 'localhost' or 'db'"
    )
    port: int = Field(
        default=5432,
        description="Database port, e.g., 5432 for PostgreSQL"
    )
    user: str = Field(
        default="postgres",
        description="Database username"
    )
    password: SecretStr = Field(
        default=...,
        description="Database password, should be kept secret"
    )
    name: str = Field(
        default="universal",
        description="Database name, e.g., 'universal'"
    )

    @model_validator(mode="before")
    @classmethod
    def build_url_from_components(cls: type[DatabaseSettings], values: dict[str, Any]) -> dict[str, Any]:
        # Only build if `url` is missing
        if values.get("url") is None:
            print(values)
            values["url"] = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values["user"],
                password=values["password"].get_secret_value() if isinstance(values["password"], SecretStr) else values["password"],
                host=values["hostname"],
                port=int(values["port"]),
                path=values["name"]
            )
        return values

class Settings(BaseSettings):
    project_name: str = Field(..., alias="name", description="Project name, e.g., 'Universal API'")
    version: str = Field(..., alias="version", description="Project version, e.g., '1.0.0'")
    description: str = Field(..., alias="description", description="Project description")
    debug: bool = Field(default=False, alias="UI_DEBUG_MODE", description="Enable debug mode")
    log_level: str = Field(default="INFO", alias="UI_LOG_LEVEL", description="Logging level for the application")
    log_file: str = Field(default="logs/app.log", alias="UI_LOG_FILE", description="Path to the log file")

    database: DatabaseSettings
    # keycloak: KeycloakSettings

    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_OVERRIDE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_max_split=1,
        env_nested_delimiter='_',
        pyproject_toml_table_header=("tool", "poetry"),
    )

    @classmethod
    def settings_customise_sources(
        cls: type[Settings],
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        override_path: str = os.environ.get("ENV_FILE_OVERRIDE", ".env")
        dotenv = DotEnvSettingsSource(
            cls,
            env_file=Path(override_path),
            env_file_encoding="utf-8",
        )
        return (
            init_settings,
            env_settings,
            dotenv,
            PyprojectTomlConfigSettingsSource(cls),
            file_secret_settings,
        )

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    return settings
