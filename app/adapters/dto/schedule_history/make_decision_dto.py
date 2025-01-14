from app.shared.dto_constants import DTOConstant
from pydantic import BaseModel


class MakeDecisionDTO(BaseModel):
    operation_value:DTOConstant.StandardVarcharField(description="Текущая операция")
    next_operation_value:DTOConstant.StandardVarcharField(description="Следующая операция")
    is_passed:DTOConstant.StandardBooleanTrueField(description="Пройден ли?")
    cancel_reason:DTOConstant.StandardNullableTextField(description="Причина отмены")
    vehicle_tara_t:DTOConstant.StandardNullablePriceField(description="Вес тары в тоннах ТС")
    vehicle_netto_t:DTOConstant.StandardNullablePriceField(description="Вес нетто в тоннах ТС")
    vehicle_brutto_t:DTOConstant.StandardNullablePriceField(description="Вес брутто в тоннах ТС")
    trailer_tara_t:DTOConstant.StandardNullablePriceField(description="Вес тары в тоннах транспорта")
    trailer_netto_t:DTOConstant.StandardNullablePriceField(description="Вес нетто в тоннах транспорта")
    trailer_brutto_t:DTOConstant.StandardNullablePriceField(description="Вес брутто в тоннах транспорта")

    class Config:
        from_attributes = True