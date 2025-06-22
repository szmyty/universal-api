from __future__ import annotations

import os
import platform
import getpass

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
from spdx_license_list import LICENSES

class KeycloakSettings(BaseModel):
    """Configuration for connecting to Keycloak OIDC server."""
    model_config = SettingsConfigDict(
        env_prefix="KEYCLOAK_",
        env_nested_delimiter="_",
    )

    hostname: str = Field(default="keycloak", description="Keycloak service host")
    http_port: int = Field(default=8080, description="Keycloak HTTP port")
    https_port: int = Field(default=8443, description="Keycloak HTTPS port")
    realm: str = Field(default="universal", description="Keycloak realm name")
    client_id: str = Field(default="universal-client", description="OIDC client ID")
    client_secret: SecretStr = Field(..., description="OIDC client secret")
    http_relative_path: str = Field(default="/auth", description="Base Keycloak path")
    swagger_client_id: str = Field(default="swagger-ui", description="Client ID used for Swagger UI OAuth2 authorization")
    verify_ssl: bool = Field(default=True, description="Whether to verify Keycloak's SSL certificate")

    @property
    def http_url(self: KeycloakSettings) -> str:
        return f"http://{self.hostname}:{self.http_port}{self.http_relative_path}"

    @property
    def https_url(self: KeycloakSettings) -> str:
        return f"https://{self.hostname}:{self.https_port}{self.http_relative_path}"

    @property
    def base_issuer_url(self: KeycloakSettings) -> str:
        return f"{self.https_url}/realms/{self.realm}"

    @property
    def openid_config_url(self: KeycloakSettings) -> str:
        return f"{self.base_issuer_url}/.well-known/openid-configuration"

    @property
    def token_url(self: KeycloakSettings) -> str:
        return f"{self.base_issuer_url}/protocol/openid-connect/token"

    @property
    def jwks_url(self: KeycloakSettings) -> str:
        return f"{self.base_issuer_url}/protocol/openid-connect/certs"

class DatabaseSettings(BaseModel):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_nested_delimiter="_",
    )

    backend: str = Field("postgresql+asyncpg", description="Database engine, e.g., 'postgresql+asyncpg' or 'sqlite'")
    url: str | PostgresDsn | None = Field(
        default=None,
        description="Full database URL (overrides other fields if set)"
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
            backend: str = str(values.get("backend", "postgresql+asyncpg"))

            if backend.startswith("sqlite"):
                # sqlite:///file.db or sqlite:///:memory:
                db_name: str = values.get("name", "sqlite.db")
                path: str = ":memory:" if db_name == ":memory:" else os.path.relpath(db_name)
                values["url"] = f"sqlite+aiosqlite:///{path}"
            elif backend.startswith("postgresql"):
                values["url"] = PostgresDsn.build(
                    scheme=backend,
                    username=values["user"],
                    password=values["password"].get_secret_value() if isinstance(values["password"], SecretStr) else values["password"],
                    host=values["hostname"],
                    port=int(values["port"]),
                    path=values["name"],
                )
            else:
                raise ValueError(f"Unsupported database backend: {backend}")

            return values

class SystemSettings(BaseModel):
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[3])
    shell: str = Field(default_factory=lambda: Path(os.environ.get("SHELL", "unknown")).name)
    os_name: str = Field(default_factory=platform.system)
    os_version: str = Field(default_factory=platform.version)
    python_version: str = Field(default_factory=lambda: platform.python_version())
    user: str = Field(default_factory=getpass.getuser)
    inside_container: bool = Field(default_factory=lambda: Path("/.dockerenv").exists())
    ci: bool = Field(default_factory=lambda: "CI" in os.environ)

class Settings(BaseSettings):
    project_name: str = Field(..., alias="name", description="Project name, e.g., 'Universal API'")
    version: str = Field(..., alias="version", description="Project version, e.g., '1.0.0'")
    description: str = Field(..., alias="description", description="Project description")
    license: str = Field(default="MIT", alias="license", description="License type, e.g., 'MIT'")
    fqdn: str = Field(default="localhost", alias="FQDN", description="Fully qualified domain name for the service")
    debug: bool = Field(default=False, alias="UI_DEBUG_MODE", description="Enable debug mode")
    log_level: str = Field(default="INFO", alias="UI_LOG_LEVEL", description="Logging level for the application")
    log_file: str = Field(default="logs/app.log", alias="UI_LOG_FILE", description="Path to the log file")
    api_prefix: str = Field(default="/api", alias="API_PREFIX", description="API URL prefix")

    database: DatabaseSettings
    keycloak: KeycloakSettings
    system: SystemSettings = Field(default_factory=SystemSettings)

    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_OVERRIDE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_max_split=1,
        env_nested_delimiter='_',
        pyproject_toml_table_header=("tool", "poetry"),
    )

    @property
    def terms_of_service(self: Settings) -> str:
        return f"https://{self.fqdn}/terms/"

    @property
    def license_info(self: Settings) -> dict[str, str]:
        from app.utils.license import get_license_info
        return get_license_info(self.license)

    @property
    def contact(self: Settings) -> dict[str, str]:
        return {
            "name": "Alan Szmyt",
            "url": f"https://{self.fqdn}/contact/",
            "email": "szmyty@gmail.com",
        }

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

    @model_validator(mode="after")
    def validate_license(self) -> Settings:
        if self.license not in LICENSES:
            raise ValueError(f"Invalid SPDX license ID: {self.license}")
        return self

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    log_dir: Path = Path(settings.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    return settings
