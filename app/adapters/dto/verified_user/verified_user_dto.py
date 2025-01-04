from typing import Optional, Self

from pydantic import BaseModel, model_validator

from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant


class VerifiedUserDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class VerifiedUserCDTO(BaseModel):
    user_id: DTOConstant.StandardUnsignedIntegerField()
    iin: DTOConstant.StandardNullableIINField()
    sid: DTOConstant.StandardNullableVarcharField()
    verified_at: DTOConstant.StandardNullableDateTimeField()
    will_act_at: DTOConstant.StandardDateTimeField()
    is_waiting_for_response: DTOConstant.StandardBooleanFalseField()
    is_verified: DTOConstant.StandardNullableBooleanField()
    is_rejected: DTOConstant.StandardNullableBooleanField()
    description: DTOConstant.StandardNullableTextField()
    response: DTOConstant.StandardNullableTextField()
    verified_by: DTOConstant.StandardNullableVarcharField()
    verified_by_sid: DTOConstant.StandardNullableVarcharField()

    @model_validator(mode="after")
    def validate_verified_and_rejected(self) -> Self:
        if self.is_verified and self.is_rejected:
            raise ValueError("Выберите 1 либо подтвержден ли отказано")
        if not self.is_verified and not self.is_rejected:
            raise ValueError("Выберите 1 либо подтвержден ли отказано")
        return self

    class Config:
        from_attributes = True


class VerifiedUserRDTO(BaseModel):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField()
    iin: DTOConstant.StandardNullableVarcharField()
    sid: DTOConstant.StandardNullableVarcharField()
    verified_at: DTOConstant.StandardNullableDateTimeField()
    will_act_at: DTOConstant.StandardDateTimeField()
    is_waiting_for_response: DTOConstant.StandardBooleanTrueField()
    is_verified: DTOConstant.StandardNullableBooleanField()
    is_rejected: DTOConstant.StandardNullableBooleanField()
    description: DTOConstant.StandardNullableTextField()
    response: DTOConstant.StandardNullableTextField()
    verified_by: DTOConstant.StandardNullableVarcharField()
    verified_by_sid: DTOConstant.StandardNullableVarcharField()

    class Config:
        from_attributes = True


class VerifiedUserWithRelationsDTO(VerifiedUserRDTO):
    user: Optional[UserRDTO] = None

    class Config:
        from_attributes = True
