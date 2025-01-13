from typing import Dict, Optional

from pydantic import BaseModel, Field, RootModel

from app.shared.dto_constants import DTOConstant


class KaspiPaymentCheckRequestDTO(BaseModel):
    command: DTOConstant.StandardVarcharField(description="Комманда check")
    txn_id: DTOConstant.StandardVarcharField(
        description="Идентификатор операции в KASPI"
    )
    sum: DTOConstant.StandardNullablePriceField(description="Сумма к зачислению")
    account: DTOConstant.StandardVarcharField(description="Номер заказа")


class FieldValueDTO(BaseModel):
    name: str = Field(..., alias="@name", description="Имя поля")
    text: str = Field(..., alias="#text", description="Значение поля")


# Используем RootModel для корневого словаря
class FieldsDTO(RootModel[Dict[str, FieldValueDTO]]):
    pass


class KaspiPaymentCheckResponseDTO(BaseModel):
    txn_id: DTOConstant.StandardVarcharField(
        description="Идентификатор операции в KASPI"
    )
    result: DTOConstant.StandardIntegerField(description="Ответ сервиса KASPI")
    sum: DTOConstant.StandardPriceField(description="Стоимость продукта в KZT")
    comment: DTOConstant.StandardNullableTextField(description="Комментарий системы")
    fields: Optional[FieldsDTO] = Field(default=None, description="Дополнительные поля")
