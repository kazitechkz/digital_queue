from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.organization.organization_dto import OrganizationRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant


class OrganizationEmployeeDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class OrganizationEmployeeCDTO(BaseModel):
    organization_id: DTOConstant.StandardUnsignedIntegerField()
    bin: DTOConstant.StandardUniqueBINField()
    employee_id: DTOConstant.StandardUnsignedIntegerField()
    sid: DTOConstant.StandardNullableVarcharField()
    request_id: DTOConstant.StandardNullableUnsignedIntegerField()

    class Config:
        from_attributes = True


class OrganizationEmployeeRDTO(OrganizationEmployeeDTO):
    organization_id: DTOConstant.StandardUnsignedIntegerField()
    bin: DTOConstant.StandardUniqueBINField()
    employee_id: DTOConstant.StandardUnsignedIntegerField()
    sid: DTOConstant.StandardNullableVarcharField()
    request_id: DTOConstant.StandardNullableUnsignedIntegerField()

    class Config:
        from_attributes = True


class OrganizationEmployeeWithRelationsDTO(OrganizationEmployeeRDTO):
    organization: Optional[OrganizationRDTO] = None
    employee: Optional[UserRDTO] = None
    # request:Optional[EmployeeRequestRDTO] = None

    class Config:
        from_attributes = True
