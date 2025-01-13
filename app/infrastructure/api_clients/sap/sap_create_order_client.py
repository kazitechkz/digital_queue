import random
from datetime import date, datetime
from typing import Optional, Union

import requests

from app.adapters.dto.sap.create_sap_order_dto import (
    CreateIndividualSapOrderDTO,
    CreateLegalSapOrderDTO,
    SapStatusDTO,
)
from app.adapters.dto.sap.sap_bearer_token_dto import SapBearerTokenDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config
from app.infrastructure.redis_client import redis_client


class SapCreateOrderApiClient:
    ACCESS_TOKEN_SAP088 = "access_token_sap088"

    async def create_sap_order(
        self, order_data: Union[CreateLegalSapOrderDTO, CreateIndividualSapOrderDTO]
    ) -> SapStatusDTO:
        if app_config.sap_use_fake_service:
            data = self._fake_create_order_response(order_data=order_data)
            items_list_data = {
                "items": [data["items"]["item"]]  # Преобразуем `item` в список
            }
            order_data = SapStatusDTO.parse_obj(items_list_data)
            return order_data
        else:
            token: str = await self.get_access_token()
            basic_url = app_config.sap_088_create_order_http_url
            if app_config.sap_088_create_order_https_enabled:
                basic_url = app_config.sap_088_create_order_https_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }
            payload = self._create_sap_order_payload(order_data=order_data)
            try:
                response = requests.post(basic_url, json=payload, headers=headers)
                response.raise_for_status()  # Проверка статуса HTTP
                data = response.json()
                items_list_data = {
                    "items": [data["items"]["item"]]  # Преобразуем `item` в список
                }
                order_data = SapStatusDTO.parse_obj(items_list_data)
                return order_data
            except requests.exceptions.RequestException as e:
                raise AppExceptionResponse.internal_error(
                    message=f"Ошибка при создании заказа в системе SAP 088 {str(e)}"
                )

    def _fake_create_order_response(
        self, order_data: Union[CreateLegalSapOrderDTO, CreateIndividualSapOrderDTO]
    ):
        zakaz = random.randint(1000000000, 9999999999)
        percentage = random.randint(0, 100)
        now = datetime.now()
        # Форматирование даты
        current_date = now.strftime("%Y-%m-%d")  # Формат YYYY-MM-DD
        # Форматирование времени
        current_time = now.strftime("%H:%M:%S")  # Формат HH:MM:SS
        if percentage > 30:
            return {
                "items": {
                    "item": {
                        "STATUS": "0",
                        "ZAKAZ": None,
                        "PDF": None,
                        "TEXT": "Не найдена позиция заказа (фейковый сервис)",
                        "DATE": f"{current_date}",
                        "TIME": f"{current_time}",
                        "ORDER_ID": order_data.ORDER_ID,
                    }
                }
            }
        else:
            return {
                "items": {
                    "item": {
                        "STATUS": "1",
                        "ZAKAZ": f"{zakaz}",
                        "PDF": "BASE64PDF",
                        "TEXT": None,
                        "DATE": f"{current_date}",
                        "TIME": f"{current_time}",
                        "ORDER_ID": order_data.ORDER_ID,
                    }
                }
            }

    def _create_sap_order_payload(
        self, order_data: Union[CreateLegalSapOrderDTO, CreateIndividualSapOrderDTO]
    ) -> dict:
        if isinstance(order_data, CreateLegalSapOrderDTO):
            payload = {
                "items": {
                    "item": [
                        {
                            "DOGOVOR": order_data.DOGOVOR,
                            "MATNR": order_data.MATNR,
                            "QUAN": order_data.QUAN,
                            "ORDER_ID": order_data.ORDER_ID,
                        }
                    ]
                }
            }
        else:
            payload = {
                "items": {
                    "item": [
                        {
                            "WERKS": order_data.WERKS,
                            "MATNR": order_data.MATNR,
                            "KUN_NAME": order_data.KUN_NAME,
                            "ADR_INDEX": order_data.ADR_INDEX,
                            "ADR_CITY": order_data.ADR_CITY,
                            "ADR_STR": order_data.ADR_STR,
                            "ADR_DOM": order_data.ADR_DOM,
                            "IIN": order_data.IIN,
                            "QUAN": order_data.QUAN,
                            "PRICE": order_data.PRICE,
                            "ORDER_ID": order_data.ORDER_ID,
                        }
                    ]
                }
            }
        return payload

    async def get_access_token(self) -> str:
        access_token: Optional[str] = redis_client.get(self.ACCESS_TOKEN_SAP088)
        if not access_token:
            token_dto = await self._make_call_to_sap_auth()
            return token_dto.access_token
        return access_token

    async def _make_call_to_sap_auth(self) -> SapBearerTokenDTO:
        payload = {
            "grant_type": app_config.sap_088_grant_type,
            "client_id": app_config.sap_088_client_id,
            "client_secret": app_config.sap_088_client_secret,
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
                self.ACCESS_TOKEN_SAP088, token_dto.expires_in, token_dto.access_token
            )
            return token_dto
        except requests.exceptions.RequestException as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ошибка при генерации токена SAP 083 {str(e)}"
            )
