from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.role.role_dto import RoleRDTO
from app.shared.dto_constants import DTOConstant


class OperationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class OperationCDTO(BaseModel):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    role_id: DTOConstant.StandardIntegerField()
    role_value: DTOConstant.StandardVarcharField()
    role_keycloak_value: DTOConstant.StandardVarcharField()
    is_first: DTOConstant.StandardBooleanFalseField()
    is_last: DTOConstant.StandardBooleanFalseField()
    prev_id: DTOConstant.StandardNullableIntegerField()
    next_id: DTOConstant.StandardNullableIntegerField()
    prev_value: DTOConstant.StandardNullableVarcharField()
    next_value: DTOConstant.StandardNullableVarcharField()
    can_cancel: DTOConstant.StandardBooleanFalseField()
    is_active: DTOConstant.StandardBooleanTrueField()

    class Config:
        from_attributes = True


class OperationRDTO(OperationDTO):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    role_id: DTOConstant.StandardNullableIntegerField()
    role_value: DTOConstant.StandardNullableVarcharField()
    role_keycloak_value: DTOConstant.StandardNullableVarcharField()
    is_first: DTOConstant.StandardBooleanFalseField()
    is_last: DTOConstant.StandardBooleanFalseField()
    prev_id: DTOConstant.StandardNullableIntegerField()
    next_id: DTOConstant.StandardNullableIntegerField()
    prev_value: DTOConstant.StandardNullableVarcharField()
    next_value: DTOConstant.StandardNullableVarcharField()
    can_cancel: DTOConstant.StandardBooleanFalseField()
    is_active: DTOConstant.StandardBooleanTrueField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class OperationWithRelationsDTO(OperationRDTO):
    prev_operation: Optional[OperationRDTO]
    next_operation: Optional[OperationRDTO]
    role: Optional[RoleRDTO]

    class Config:
        from_attributes = True
