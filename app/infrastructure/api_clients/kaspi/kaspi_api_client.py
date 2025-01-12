import requests
from app.adapters.dto.kaspi.kaspi_request_dto import KaspiFastPaymentResponseDTO, KaspiFastPaymentDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config


class KaspiPaymentApiClient:

    async def fast_payments(self,dto:KaspiFastPaymentDTO)->KaspiFastPaymentResponseDTO:
        kaspi_url = app_config.fast_payment_kaspi_url
        payload = {
            "TranId": f"{dto.TranId}",
            "OrderId": f"{dto.OrderId}",
            "Amount": dto.Amount,
            "Service": dto.Service,
            "returnUrl": f"{dto.returnUrl}",
            "refererHost": f"{dto.refererHost}",
            "GenerateQrCode": f"{dto.GenerateQrCode}",
        }
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(kaspi_url, json=payload, headers=headers)
            response.raise_for_status()  # Проверка статуса HTTP
            data = response.json()
            order_data = KaspiFastPaymentResponseDTO.parse_obj(data)
            return order_data
        except requests.exceptions.RequestException as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ошибка при оплате Каспи попробуйте позже"
            )