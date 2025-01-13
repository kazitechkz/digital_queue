from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.user.user_dto import UserOrganizationRDTO, UserRDTO
from app.shared.dto_constants import DTOConstant


class EmployeeRequestDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class EmployeeRequestCDTO(EmployeeRequestDTO):
    organization_id: DTOConstant.StandardIntegerField()
    organization_full_name: DTOConstant.StandardNullableVarcharField()
    organization_bin: DTOConstant.StandardNullableVarcharField()

    owner_id: DTOConstant.StandardNullableIntegerField()
    owner_name: DTOConstant.StandardVarcharField()
    owner_sid: DTOConstant.StandardNullableVarcharField()

    employee_id: DTOConstant.StandardIntegerField()
    employee_name: DTOConstant.StandardVarcharField()
    employee_email: DTOConstant.StandardVarcharField()
    employee_sid: DTOConstant.StandardNullableVarcharField()

    status: DTOConstant.StandardNullableIntegerField()
    requested_at: DTOConstant.StandardDateTimeField()
    decided_at: DTOConstant.StandardNullableDateTimeField()

    class Config:
        from_attributes = True


class EmployeeRequestRDTO(EmployeeRequestDTO):
    organization_id: DTOConstant.StandardIntegerField()
    organization_full_name: DTOConstant.StandardNullableVarcharField()
    organization_bin: DTOConstant.StandardNullableVarcharField()

    owner_id: DTOConstant.StandardNullableIntegerField()
    owner_name: DTOConstant.StandardVarcharField()
    owner_sid: DTOConstant.StandardNullableVarcharField()

    employee_id: DTOConstant.StandardIntegerField()
    employee_name: DTOConstant.StandardVarcharField()
    employee_email: DTOConstant.StandardVarcharField()
    employee_sid: DTOConstant.StandardNullableVarcharField()

    status: DTOConstant.StandardNullableIntegerField()
    requested_at: DTOConstant.StandardDateTimeField()
    decided_at: DTOConstant.StandardNullableDateTimeField()

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class EmployeeRequestWithRelationsDTO(EmployeeRequestRDTO):
    owner: Optional[UserRDTO] = None
    employee: Optional[UserRDTO] = None
    organization: Optional[UserOrganizationRDTO] = None

    class Config:
        from_attributes = True


class EmployeeRequestOwnerCDTO(BaseModel):
    organization_id: DTOConstant.StandardIntegerField()
    employee_id: DTOConstant.StandardIntegerField()

    class Config:
        from_attributes = True


class EmployeeRequestClientCDTO(BaseModel):
    status: DTOConstant.StandardIntegerField()

    class Config:
        from_attributes = True
