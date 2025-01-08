from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.organization_type.organization_type_dto import \
    OrganizationTypeRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant


class OrganizationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class OrganizationCDTO(BaseModel):
    owner_id: DTOConstant.StandardUnsignedIntegerField()
    type_id: DTOConstant.StandardUnsignedIntegerField()
    file_id: DTOConstant.StandardNullableIntegerField()
    full_name: DTOConstant.StandardTextField()
    short_name: DTOConstant.StandardTextField()
    bin: DTOConstant.StandardUniqueBINField()
    bik: DTOConstant.StandardNullableVarcharField()
    kbe: DTOConstant.StandardNullableVarcharField()
    email: DTOConstant.StandardEmailField()
    phone: DTOConstant.StandardPhoneField()
    address: DTOConstant.StandardNullableTextField()
    status: DTOConstant.StandardBooleanTrueField()
    is_verified: DTOConstant.StandardNullableBooleanField()

    class Config:
        from_attributes = True


class OrganizationRDTO(OrganizationDTO):
    owner_id: DTOConstant.StandardNullableUnsignedIntegerField()
    type_id: DTOConstant.StandardNullableUnsignedIntegerField()
    file_id: DTOConstant.StandardNullableIntegerField()
    full_name: DTOConstant.StandardTextField()
    short_name: DTOConstant.StandardTextField()
    bin: DTOConstant.StandardUniqueBINField()
    bik: DTOConstant.StandardNullableVarcharField()
    kbe: DTOConstant.StandardNullableVarcharField()
    email: DTOConstant.StandardEmailField()
    phone: DTOConstant.StandardPhoneField()
    address: DTOConstant.StandardNullableTextField()
    status: DTOConstant.StandardBooleanTrueField()
    is_verified: DTOConstant.StandardNullableBooleanField()

    class Config:
        from_attributes = True


class OrganizationWithRelationsDTO(OrganizationRDTO):
    owner: Optional[UserRDTO] = None
    type: Optional[OrganizationTypeRDTO] = None
    file: Optional[FileRDTO] = None
