from __future__ import annotations

from pydantic import PostgresDsn
import pytest
from app.core.settings import Settings, KeycloakSettings, DatabaseSettings

@pytest.mark.unit
@pytest.mark.usefixtures("settings")
class TestSettings:
    """Test the Settings class."""

    def test_settings_instance(self: TestSettings, settings: Settings) -> None:
        """Ensure the settings instance is created correctly."""
        assert isinstance(settings, Settings)

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

#     def test_keycloak_settings(self: TestSettings, fresh_settings: Settings):
#         kc: KeycloakSettings = fresh_settings.keycloak
#         assert kc.hostname == "auth.test"
#         assert kc.realm == "testrealm"
#         assert kc.http_url.startswith("http://")
#         assert kc.https_url.startswith("https://")
