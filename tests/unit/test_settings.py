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
        db: DatabaseSettings = settings.database
        assert db.hostname == "test.localhost"
        assert db.port == 5432
        assert db.name == "universal_test"
        assert db.user == "testuser"
        assert db.url == PostgresDsn(url="postgresql+asyncpg://testuser:testpass@test.localhost:5432/universal_test")

#     def test_keycloak_settings(self: TestSettings, fresh_settings: Settings):
#         kc: KeycloakSettings = fresh_settings.keycloak
#         assert kc.hostname == "auth.test"
#         assert kc.realm == "testrealm"
#         assert kc.http_url.startswith("http://")
#         assert kc.https_url.startswith("https://")

#     def test_app_metadata(self: TestSettings, fresh_settings: Settings):
#         s: Settings = fresh_settings
#         assert s.project_name.lower() == "universal api"
#         assert s.version.count(".") == 2
#         assert s.description != ""
#         assert s.log_level.upper() == "DEBUG"
