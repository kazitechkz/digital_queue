from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class KaspiFastPaymentDTO(BaseModel):
    TranId: DTOConstant.StandardVarcharField(description="Номер транзакции, номер заказа")
    OrderId:DTOConstant.StandardVarcharField(description="Номер транзакции, номер заказа SAP")
    Amount:DTOConstant.StandardIntegerField(description="Сумма оплаты в тиынах")
    Service: DTOConstant.StandardIntegerField(description="Уникальная строка сервиса")
    returnUrl: DTOConstant.StandardVarcharField(description="Адрес страницы для возврата после проведения платежа")
    refererHost: DTOConstant.StandardVarcharField(description="Домен, с которого происходит отправка запроса (только для JSON запроса)")
    GenerateQrCode: DTOConstant.StandardBooleanTrueField(description="Флаг для получения картинки с QR в формате base 64 (только для JSON запроса)")

class KaspiFastPaymentResponseDTO(BaseModel):
    code:DTOConstant.StandardIntegerField(description="Ответ где 0 - успешно")
    redirectUrl: DTOConstant.StandardNullableVarcharField(description="Ссылка перехода в приложение Каспи")
    message:DTOConstant.StandardNullableTextField(description="Сообщение с ошибкой")
    qrCodeImage:DTOConstant.StandardNullableTextField(description="Base64 QR кода оплаты")


class KaspiFastPaymentFrontendRequestDTO(BaseModel):
    order_id:DTOConstant.StandardIntegerField(description="Номер заказа")
    generate_qr_code:DTOConstant.StandardBooleanTrueField(description="Сгенерировать QR код?")