from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class KaspiPaymentDTO(BaseModel):
    id:DTOConstant.StandardID()

    class Config:
        from_attributes = True


class KaspiPaymentCDTO(BaseModel):
    order_id: DTOConstant.StandardNullableIntegerField()
    zakaz: DTOConstant.StandardVarcharField()
    txn_id: DTOConstant.StandardNullableVarcharField()
    txn_check_id: DTOConstant.StandardNullableVarcharField()
    txn_pay_id: DTOConstant.StandardNullableVarcharField()
    txn_date: DTOConstant.StandardNullableVarcharField()
    command: DTOConstant.StandardNullableVarcharField()
    sum: DTOConstant.StandardPriceField()
    amount: DTOConstant.StandardIntegerField()
    is_failed: DTOConstant.StandardBooleanFalseField()
    is_paid: DTOConstant.StandardBooleanFalseField()
    is_qr_generate: DTOConstant.StandardBooleanFalseField()
    paid_at: DTOConstant.StandardNullableDateField()

    class Config:
        from_attributes = True

class KaspiPaymentRDTO(KaspiPaymentDTO):
    order_id:DTOConstant.StandardNullableIntegerField()
    zakaz:DTOConstant.StandardVarcharField()
    txn_id:DTOConstant.StandardNullableVarcharField()
    txn_check_id:DTOConstant.StandardNullableVarcharField()
    txn_pay_id:DTOConstant.StandardNullableVarcharField()
    txn_date:DTOConstant.StandardNullableVarcharField()
    command:DTOConstant.StandardNullableVarcharField()
    sum:DTOConstant.StandardPriceField()
    amount:DTOConstant.StandardIntegerField()
    is_failed:DTOConstant.StandardBooleanFalseField()
    is_paid:DTOConstant.StandardBooleanFalseField()
    is_qr_generate:DTOConstant.StandardBooleanFalseField()
    paid_at:DTOConstant.StandardNullableDateField()

    class Config:
        from_attributes = True

