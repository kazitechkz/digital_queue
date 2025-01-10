from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class SapRequestDTO(BaseModel):
    id:DTOConstant.StandardID()

    class Config:
        from_attributes = True

class SapRequestCDTO(BaseModel):
    order_id:DTOConstant.StandardIntegerField()
    werks:DTOConstant.StandardVarcharField()
    matnr:DTOConstant.StandardVarcharField()
    kun_name:DTOConstant.StandardNullableVarcharField()
    iin:DTOConstant.StandardNullableVarcharField()
    quan:DTOConstant.StandardPriceField()
    price:DTOConstant.StandardPriceField()
    dogovor:DTOConstant.StandardNullableVarcharField()

    status:DTOConstant.StandardNullableVarcharField()
    zakaz:DTOConstant.StandardNullableVarcharField()
    text:DTOConstant.StandardNullableTextField()
    pdf:DTOConstant.StandardNullableTextField()
    date:DTOConstant.StandardNullableDateField()
    time:DTOConstant.StandardNullableTimeField()

    is_active: DTOConstant.StandardBooleanTrueField()
    is_failed: DTOConstant.StandardBooleanFalseField()
    is_paid: DTOConstant.StandardBooleanFalseField()

    class Config:
        from_attributes = True


class SapRequestRDTO(SapRequestDTO):
    order_id: DTOConstant.StandardNullableIntegerField()
    werks: DTOConstant.StandardNullableVarcharField()
    matnr: DTOConstant.StandardVarcharField()
    kun_name: DTOConstant.StandardNullableVarcharField()
    iin: DTOConstant.StandardNullableVarcharField()
    quan: DTOConstant.StandardPriceField()
    price: DTOConstant.StandardPriceField()
    dogovor: DTOConstant.StandardNullableVarcharField()

    status: DTOConstant.StandardNullableVarcharField()
    zakaz: DTOConstant.StandardNullableVarcharField()
    text: DTOConstant.StandardNullableTextField()
    pdf: DTOConstant.StandardNullableTextField()
    date: DTOConstant.StandardNullableDateField()
    time: DTOConstant.StandardNullableTimeField()

    is_active: DTOConstant.StandardBooleanTrueField()
    is_failed: DTOConstant.StandardBooleanFalseField()
    is_paid: DTOConstant.StandardBooleanFalseField()

    class Config:
        from_attributes = True

