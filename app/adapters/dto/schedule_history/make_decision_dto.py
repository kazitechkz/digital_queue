from app.shared.dto_constants import DTOConstant
from pydantic import BaseModel


class MakeDecisionDTO(BaseModel):
    next_operation_value:DTOConstant.StandardNullableVarcharField(description="Следующая операция")
    is_passed:DTOConstant.StandardBooleanTrueField(description="Пройден ли?")
    cancel_reason:DTOConstant.StandardNullableTextField(description="Причина отмены")
    vehicle_tara_t:DTOConstant.StandardNullablePriceField(description="Вес тары в тоннах ТС")
    vehicle_netto_t:DTOConstant.StandardNullablePriceField(description="Вес нетто в тоннах ТС")
    vehicle_brutto_t:DTOConstant.StandardNullablePriceField(description="Вес брутто в тоннах ТС")

    class Config:
        from_attributes = True