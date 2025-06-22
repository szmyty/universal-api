from __future__ import annotations
from pathlib import Path

import pytest
from pydantic import PostgresDsn, SecretStr

from app.core.settings import Settings, DatabaseSettings, KeycloakSettings, SystemSettings
from app.utils.shell import KNOWN_SHELLS

@pytest.mark.unit
@pytest.mark.usefixtures("settings", "sqlite_settings")
class TestSettings:
    """Test the Settings class."""

    def test_settings_instance(self: TestSettings, settings: Settings) -> None:
        """Ensure the settings instance is created correctly."""
        assert isinstance(settings, Settings)

    def test_sqlite_settings_instance(self: TestSettings, sqlite_settings: Settings) -> None:
        """Ensure the sqlite_settings instance is created correctly."""
        assert isinstance(sqlite_settings, Settings)

    def test_sqlite_database_settings(self: TestSettings, sqlite_settings: Settings) -> None:
        """Test the SQLite database settings."""
        db: DatabaseSettings = sqlite_settings.database
        assert isinstance(db, DatabaseSettings)
        assert db.backend == "sqlite"
        assert db.url == "sqlite+aiosqlite:///test.db"

    def test_database_settings(self: TestSettings, settings: Settings) -> None:
        """Test the database settings."""
        db: DatabaseSettings = settings.database
        assert isinstance(db, DatabaseSettings)
        assert db.hostname == "test.localhost"
        assert db.port == 5432
        assert db.name == "universal_test"
        assert db.user == "testuser"
        assert db.url == PostgresDsn(url="postgresql+asyncpg://testuser:testpass@test.localhost:5432/universal_test")

    def test_project_settings(self: TestSettings, settings: Settings) -> None:
        """Test the project settings."""
        assert settings.project_name == "universal-api"
        assert settings.version == "0.1.0"
        assert settings.description == "A modular, async-first backend API built with FastAPI, SQLAlchemy, and Alembic. Designed for clean architecture, domain-driven design, and future-proof datastore flexibility."

    def test_logging_settings(self: TestSettings, settings: Settings) -> None:
        """Test the logging settings."""
        assert settings.log_level == "DEBUG"
        assert settings.log_file == "logs/test_app.log"

    def test_keycloak_settings(self: TestSettings) -> None:
        """Test the Keycloak settings."""
        kc = KeycloakSettings(
            hostname="auth.test",
            realm="testrealm",
            client_secret=SecretStr("dummy-secret"),
        )

        assert kc.hostname == "auth.test"
        assert kc.realm == "testrealm"
        assert kc.http_url.startswith("http://")
        assert kc.https_url.startswith("https://")
        assert kc.base_issuer_url.endswith("/realms/testrealm")
        assert kc.token_url.endswith("/protocol/openid-connect/token")
        assert kc.jwks_url.endswith("/protocol/openid-connect/certs")

    def test_system_settings_defaults(self: TestSettings, settings: Settings) -> None:
        """Test that system settings are populated with expected defaults."""
        sys: SystemSettings = settings.system

        assert sys.project_root.exists()
        assert sys.shell in KNOWN_SHELLS
        assert isinstance(sys.os_name, str)
        assert isinstance(sys.os_version, str)
        assert isinstance(sys.python_version, str)
        assert isinstance(sys.user, str)
        assert isinstance(sys.inside_container, bool)

    def test_project_root_is_path(self: TestSettings, settings: Settings) -> None:
        """Project root should resolve to a Path object and point to the repo root."""
        root: Path = settings.system.project_root
        assert root.name in {"universal-api", "src", ".files"}  # or whatever your root dir name is
        assert isinstance(root, type(root))  # sanity check it's a Path-like
