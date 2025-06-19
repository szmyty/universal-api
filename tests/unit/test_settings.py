from __future__ import annotations

import pytest
from app.core.settings import Settings, KeycloakSettings, DatabaseSettings

@pytest.mark.unit
def test_test():
    """Dummy test to ensure pytest is working."""
    assert True

# @pytest.mark.unit
# @pytest.mark.usefixtures("fresh_settings")
# def test_debug_settings(fresh_settings):
#     print("\n[DEBUG] Dumped settings:")
#     print(fresh_settings.model_dump_json(indent=2))
#     assert True  # dummy assert to keep it valid

# @pytest.mark.unit
# class TestSettings:
#     """Test the Settings class."""

#     def test_settings_instance(self: TestSettings, fresh_settings: Settings):
#         """Ensure the settings instance is created correctly."""
#         assert isinstance(fresh_settings, Settings)

#     def test_database_settings(self: TestSettings, fresh_settings: Settings):
#         db: DatabaseSettings = fresh_settings.database
#         assert db.hostname == "localhost"
#         assert db.user == "testuser"
#         assert db.url == "postgresql+asyncpg://testuser:testpass@localhost:5432/universal_test"

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
