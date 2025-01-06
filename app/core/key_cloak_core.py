from keycloak import KeycloakOpenID

from app.infrastructure.config import app_config

keycloak_openid = KeycloakOpenID(
    server_url=app_config.keycloak_server_url,
    realm_name=app_config.keycloak_realm,
    client_id=app_config.keycloak_client_id,
    client_secret_key=app_config.keycloak_client_secret,
    verify=False,  # Отключение проверки сертификатов
)


def get_openid_config():
    return keycloak_openid.well_known()
