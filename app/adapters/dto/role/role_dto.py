from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class RoleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class RoleCDTO(BaseModel):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    keycloak_id: DTOConstant.StandardNullableVarcharField()
    keycloak_value: DTOConstant.StandardVarcharField()
    is_active: DTOConstant.StandardBooleanTrueField()

    class Config:
        from_attributes = True


class RoleRDTO(RoleDTO):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    keycloak_id: DTOConstant.StandardNullableVarcharField()
    keycloak_value: DTOConstant.StandardVarcharField()
    is_active: DTOConstant.StandardBooleanTrueField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True
