from typing import List, Optional

import requests

from app.adapters.dto.sap.sap_bearer_token_dto import SapBearerTokenDTO
from app.adapters.dto.sap.sap_contract_dto import (
    SapContractDTO,
    SapContractForResponseDTO,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config
from app.infrastructure.redis_client import redis_client
from app.shared.dto_constants import DTOConstant


class SapGetContractApiClient:
    ACCESS_TOKEN_SAP083 = "access_token_sap083"

    async def get_organization_contracts_by_bin_response(
        self, bin: DTOConstant.StandardUniqueBINField()
    ) -> List[SapContractForResponseDTO]:
        contract = await self.get_organization_contracts_by_bin(bin)

        def parse_float(value: Optional[str]) -> float:
            """
            Преобразует строку в float, удаляя лишние символы (пробелы, запятые) и заменяя разделитель.
            """
            if not value or value.strip() == "":
                return 0.0
            try:
                # Удаляем пробелы, форматируем число
                return float(value.replace(".", "").replace(",", ".").strip())
            except ValueError:
                return 0.0  # Если преобразование не удалось, возвращаем 0.0

        response_list = []

        if not contract.row:
            return response_list  # Если данных нет, возвращаем пустой список

        for row in contract.row:
            if not row.item:
                continue  # Пропускаем, если элементы item отсутствуют

            for item in row.item:
                response_dto = SapContractForResponseDTO(
                    dogovor=row.KTEXT,
                    material_sap_id=item.MATNR,
                    total_price=parse_float(item.ZWERT),
                    rest_price=parse_float(item.ZWERT_RST),
                    quan_t=parse_float(item.ZMENG),
                    quan_t_left=parse_float(item.ZMENG_RST),
                )
                response_list.append(response_dto)

        return response_list

    async def get_organization_contracts_by_bin(
        self, bin: DTOConstant.StandardUniqueBINField()
    ) -> SapContractDTO:
        token: str = await self.get_access_token()
        basic_url = app_config.sap_083_http_url
        if app_config.sap_083_https_enabled:
            basic_url = app_config.sap_083_https_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"BIN_PARTNER": bin}
        try:
            response = requests.post(basic_url, json=payload, headers=headers)
            response.raise_for_status()  # Проверка статуса HTTP
            data = response.json()
            contracts_dto = SapContractDTO.parse_obj(data)
            return contracts_dto
        except requests.exceptions.RequestException as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ошибка при получении договоров организации SAP 083 {str(e)}"
            )

    async def get_access_token(self) -> str:
        access_token: Optional[str] = redis_client.get(self.ACCESS_TOKEN_SAP083)
        if not access_token:
            token_dto = await self._make_call_to_sap_auth()
            return token_dto.access_token
        return access_token

    async def _make_call_to_sap_auth(self) -> SapBearerTokenDTO:
        payload = {
            "grant_type": app_config.sap_083_grant_type,
            "client_id": app_config.sap_083_client_id,
            "client_secret": app_config.sap_083_client_secret,
            "scope": app_config.sap_083_scope,
        }
        basic_url = app_config.sap_auth_http_url
        if app_config.auth_contract_https_enabled:
            basic_url = app_config.sap_auth_https_url

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(basic_url, data=payload, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            token_dto = SapBearerTokenDTO.parse_obj(token_data)
            redis_client.setex(
                self.ACCESS_TOKEN_SAP083, token_dto.expires_in, token_dto.access_token
            )
            return token_dto
        except requests.exceptions.RequestException as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ошибка при генерации токена SAP 083 {str(e)}"
            )
