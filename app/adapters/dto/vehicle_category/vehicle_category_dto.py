from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class VehicleCategoryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class VehicleCategoryCDTO(BaseModel):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()

    class Config:
        from_attributes = True


class VehicleCategoryRDTO(VehicleCategoryDTO):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True
