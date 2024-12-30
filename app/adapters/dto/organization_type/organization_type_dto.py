from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class OrganizationTypeDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class OrganizationTypeCDTO(BaseModel):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()

    class Config:
        from_attributes = True


class OrganizationTypeRDTO(OrganizationTypeDTO):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True
