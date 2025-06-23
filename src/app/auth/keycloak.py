from fastapi_keycloak_middleware import KeycloakConfiguration, FastApiUser, AuthorizationMethod

from app.core.settings import get_settings, Settings

# Initialize Keycloak configuration
settings: Settings = get_settings()

keycloak = KeycloakConfiguration(
    realm=settings.keycloak.realm,
    url=settings.keycloak.https_url,
    client_id=settings.keycloak.client_id,
    swagger_client_id=settings.keycloak.swagger_client_id,
    client_secret=settings.keycloak.client_secret.get_secret_value(),
    claims=[
        "openid",
        "sub",
        "name",
        "family_name",
        "given_name",
        "preferred_username",
        "email",
        "roles",
    ],
    reject_on_missing_claim=False,
    authentication_scheme="Bearer",
    authorization_method=AuthorizationMethod.NONE,
    authorization_claim="roles",
    use_introspection_endpoint=False,
    enable_device_authentication=False,
    device_authentication_claim="is_device",
    verify=settings.keycloak.verify_ssl,
    validate_token=True,
    validation_options={},
    enable_websocket_support=True,
    websocket_cookie_name="access_token"
)

excluded_endpoints: list[str] = [
    "^/health/?$"
]
