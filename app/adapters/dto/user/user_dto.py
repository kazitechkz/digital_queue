from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.role.role_dto import RoleRDTO
from app.adapters.dto.user_type.user_type_dto import UserTypeRDTO
from app.shared.dto_constants import DTOConstant


class UserDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class UserCDTO(BaseModel):
    sid: DTOConstant.StandardVarcharField()
    iin: DTOConstant.StandardUniqueIINField()
    role_id: DTOConstant.StandardIntegerField()
    type_id: DTOConstant.StandardIntegerField()
    file_id: DTOConstant.StandardNullableIntegerField()
    name: DTOConstant.StandardVarcharField()
    given_name: DTOConstant.StandardVarcharField()
    family_name: DTOConstant.StandardVarcharField()
    preferred_username: DTOConstant.StandardVarcharField()
    email: DTOConstant.StandardEmailField()
    email_verified: DTOConstant.StandardBooleanFalseField()
    phone: DTOConstant.StandardPhoneField()
    phone_verified: DTOConstant.StandardBooleanFalseField()
    tabn: DTOConstant.StandardNullableVarcharField()
    status: DTOConstant.StandardBooleanTrueField()
    password_hash: DTOConstant.StandardNullableTextField()

    class Config:
        from_attributes = True


class UserRDTO(UserDTO):
    sid: DTOConstant.StandardVarcharField()
    iin: DTOConstant.StandardNullableVarcharField()
    role_id: DTOConstant.StandardNullableIntegerField()
    type_id: DTOConstant.StandardNullableIntegerField()
    file_id: DTOConstant.StandardNullableIntegerField()
    name: DTOConstant.StandardVarcharField()
    given_name: DTOConstant.StandardNullableVarcharField()
    family_name: DTOConstant.StandardNullableVarcharField()
    preferred_username: DTOConstant.StandardVarcharField()
    email: DTOConstant.StandardEmailField()
    email_verified: DTOConstant.StandardBooleanFalseField()
    phone: DTOConstant.StandardNullableVarcharField()
    phone_verified: DTOConstant.StandardBooleanFalseField()
    tabn: DTOConstant.StandardNullableVarcharField()
    status: DTOConstant.StandardBooleanTrueField()

    class Config:
        from_attributes = True


class UserPasswordDTO(BaseModel):
    password: DTOConstant.StandardTextField()
    confirm_password: DTOConstant.StandardTextField()

    class Config:
        from_attributes = True

class UserKeycloakCDTO(BaseModel):
    sid: DTOConstant.StandardNullableVarcharField()
    iin: DTOConstant.StandardNullableVarcharField()
    role_id: DTOConstant.StandardNullableIntegerField()
    type_id: DTOConstant.StandardNullableIntegerField()
    file_id: DTOConstant.StandardNullableIntegerField()
    name: DTOConstant.StandardVarcharField()
    given_name: DTOConstant.StandardVarcharField()
    family_name: DTOConstant.StandardVarcharField()
    preferred_username: DTOConstant.StandardVarcharField()
    email: DTOConstant.StandardEmailField()
    email_verified: DTOConstant.StandardBooleanFalseField()
    phone: DTOConstant.StandardNullableVarcharField()
    phone_verified: DTOConstant.StandardBooleanFalseField()
    tabn: DTOConstant.StandardNullableVarcharField()
    status: DTOConstant.StandardBooleanTrueField()
    password_hash: DTOConstant.StandardNullableTextField()

    class Config:
        from_attributes = True


class UserWithRelationsDTO(UserRDTO):
    role: Optional[RoleRDTO] = None
    user_type: Optional[UserTypeRDTO] = None
    file: Optional[FileRDTO] = None
    # organizations:Optional[list["OrganizationRDTO"]] = None
    class Config:
        from_attributes = True
