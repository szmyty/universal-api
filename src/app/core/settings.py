from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, Field, SecretStr
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

    hostname: str
    port: int = 5432
    user: str = "postgres"
    password: SecretStr
    name: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}"
            f"@{self.hostname}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    project_name: str = Field(default="Universal API")
    version: str = Field(default="0.1.0")
    description: str = Field(default="Default project description")

    debug: bool = False
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_json: bool = False

    # database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    # keycloak: KeycloakSettings = Field(default_factory=KeycloakSettings)

    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_OVERRIDE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
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
