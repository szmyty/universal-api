from fastapi_keycloak_middleware import KeycloakConfiguration, setup_keycloak_middleware, FastApiUser, AuthorizationMethod

from app.core.settings import get_settings

# Initialize Keycloak configuration
settings = get_settings()

keycloak = KeycloakConfiguration(
    realm=settings.keycloak.realm,
    url=settings.keycloak.url,
    client_id=settings.keycloak.client_id,
    swagger_client_id=settings.keycloak.swagger_client_id,
    client_secret=settings.keycloak.client_secret,
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
    authorization_method=AuthorizationMethod.NONE
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
