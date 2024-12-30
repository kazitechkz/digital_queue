from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class VehicleColorDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class VehicleColorCDTO(BaseModel):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()

    class Config:
        from_attributes = True


class VehicleColorRDTO(VehicleColorDTO):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True
