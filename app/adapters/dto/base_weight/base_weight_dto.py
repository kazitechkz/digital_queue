from typing import Optional

from app.adapters.dto.vehicle.vehicle_dto import VehicleRDTO
from app.shared.dto_constants import DTOConstant
from pydantic import BaseModel


class BaseWeightDTO(BaseModel):
    id:DTOConstant.StandardID()

    class Config:
        from_attributes = True

class BaseWeightRDTO(BaseWeightDTO):
    vehicle_id:DTOConstant.StandardNullableIntegerField()
    car_number:DTOConstant.StandardNullableVarcharField()
    vehicle_tara_kg:DTOConstant.StandardIntegerField()
    measured_at:DTOConstant.StandardDateTimeField()
    measured_to:DTOConstant.StandardDateTimeField()

    created_at:DTOConstant.StandardCreatedAt()
    updated_at:DTOConstant.StandardUpdatedAt()
    class Config:
        from_attributes = True


class BaseWeightCDTO(BaseModel):
    vehicle_id: DTOConstant.StandardNullableIntegerField()
    car_number: DTOConstant.StandardVarcharField()
    vehicle_tara_kg: DTOConstant.StandardIntegerField()
    measured_at: DTOConstant.StandardDateTimeField()
    measured_to: DTOConstant.StandardDateTimeField()
    class Config:
        from_attributes = True

class BaseWeightWithRelationsDTO(BaseWeightRDTO):
    vehicle:Optional[VehicleRDTO] = None
    class Config:
        from_attributes = True