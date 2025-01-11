import requests
from app.adapters.dto.kaspi.kaspi_request_dto import KaspiFastPaymentResponseDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config


class KaspiPaymentApiClient:

    async def fast_payments(self,KaspiFastPaymentDTO):
        kaspi_url = app_config.fast_payment_kaspi_url
        payload = {
            "TranId": f"{KaspiFastPaymentDTO.TranId}",
            "OrderId": f"{KaspiFastPaymentDTO.OrderId}",
            "Amount": KaspiFastPaymentDTO.Amount,
            "Service": KaspiFastPaymentDTO.Service,
            "returnUrl": f"{KaspiFastPaymentDTO.ReturnUrl}",
            "refererHost": f"{KaspiFastPaymentDTO.RefererHost}",
            "GenerateQrCode": f"{KaspiFastPaymentDTO.GenerateQrCode}",
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