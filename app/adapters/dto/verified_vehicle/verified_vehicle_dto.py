from typing import Optional, Self

from pydantic import BaseModel, model_validator

from app.adapters.dto.vehicle.vehicle_dto import VehicleRDTO
from app.shared.dto_constants import DTOConstant


class VerifiedVehicleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class VerifiedVehicleCDTO(BaseModel):
    vehicle_id: DTOConstant.StandardUnsignedIntegerField()
    car_number: DTOConstant.StandardCarNumberField()
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


class VerifiedVehicleRDTO(BaseModel):
    vehicle_id: DTOConstant.StandardNullableUnsignedIntegerField()
    car_number: DTOConstant.StandardNullableVarcharField()
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


class VerifiedVehicleWithRelationsDTO(VerifiedVehicleRDTO):
    vehicle: Optional[VehicleRDTO] = None

    class Config:
        from_attributes = True
