import requests

from app.adapters.dto.sap.sap_bearer_token_dto import SapBearerTokenDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config
from app.infrastructure.redis_client import redis_client


class SapCreateOrderApiClient:
    ACCESS_TOKEN_SAP088="access_token_sap088"







    async def _make_call_to_sap_auth(self)->SapBearerTokenDTO:
        payload = {
            "grant_type": app_config.sap_088_grant_type,
            "client_id": app_config.sap_088_client_id,
            "client_secret": app_config.sap_088_client_secret,
        }
        basic_url = app_config.sap_auth_http_url
        if app_config.auth_contract_https_enabled:
            basic_url = app_config.sap_auth_https_url

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(basic_url, data=payload, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            token_dto = SapBearerTokenDTO.parse_obj(token_data)
            redis_client.setex(self.ACCESS_TOKEN_SAP088, token_dto.expires_in, token_dto.access_token)
            return token_dto
        except requests.exceptions.RequestException as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ошибка при генерации токена SAP 083 {str(e)}"
            )