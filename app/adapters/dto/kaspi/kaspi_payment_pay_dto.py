from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class KaspiPaymentPayRequestDTO(BaseModel):
    command:DTOConstant.StandardVarcharField(description="Комманда pay")
    txn_id:DTOConstant.StandardVarcharField(description="Идентификатор операции в KASPI")
    sum:DTOConstant.StandardPriceField(description="Сумма к зачислению")
    account:DTOConstant.StandardVarcharField(description="Номер заказа")
    txn_date:DTOConstant.StandardVarcharField(description="Дата оплаты заказа")

class KaspiPaymentPayResponseDTO(BaseModel):
    txn_id:DTOConstant.StandardVarcharField(description="Идентификатор операции в KASPI")
    prv_txn_id:DTOConstant.StandardVarcharField(description="Идентификатор операции в KASPI")
    result:DTOConstant.StandardIntegerField(description="Ответ сервиса KASPI")
    sum:DTOConstant.StandardPriceField(description="Стоимость продукта в KZT")
    comment:DTOConstant.StandardNullableTextField(description="Комментарий системы")