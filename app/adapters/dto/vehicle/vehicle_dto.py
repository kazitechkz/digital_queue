from typing import Optional

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.organization.organization_dto import OrganizationRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.adapters.dto.vehicle_category.vehicle_category_dto import \
    VehicleCategoryRDTO
from app.adapters.dto.vehicle_color.vehicle_color_dto import VehicleColorRDTO
from app.shared.dto_constants import DTOConstant


class VehicleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class VehicleCDTO(BaseModel):
    category_id: DTOConstant.StandardUnsignedIntegerField()
    color_id: DTOConstant.StandardUnsignedIntegerField()
    owner_id: DTOConstant.StandardNullableUnsignedIntegerField()
    organization_id: DTOConstant.StandardNullableUnsignedIntegerField()
    file_id: DTOConstant.StandardNullableUnsignedIntegerField()
    registration_number: DTOConstant.StandardCarNumberField()
    car_model: DTOConstant.StandardVarcharField()
    is_trailer: DTOConstant.StandardBooleanFalseField()
    vehicle_info: DTOConstant.StandardNullableTextField()

    @model_validator(mode="after")
    def check_owner_and_organization(self) -> Self:
        if (self.owner_id is not None and self.organization_id is not None) or (
            self.owner_id is None and self.organization_id is None
        ):
            raise ValueError(
                "Должно быть заполнено только одно из полей: Владелец или Организация."
            )
        return self

    class Config:
        from_attributes = True


class VehicleRDTO(VehicleDTO):
    category_id: DTOConstant.StandardNullableUnsignedIntegerField()
    color_id: DTOConstant.StandardNullableUnsignedIntegerField()
    owner_id: DTOConstant.StandardNullableUnsignedIntegerField()
    organization_id: DTOConstant.StandardNullableUnsignedIntegerField()
    file_id: DTOConstant.StandardNullableUnsignedIntegerField()
    registration_number: DTOConstant.StandardCarNumberField()
    car_model: DTOConstant.StandardVarcharField()
    is_trailer: DTOConstant.StandardBooleanFalseField()
    vehicle_info: DTOConstant.StandardNullableTextField()

    class Config:
        from_attributes = True


class VehicleWithRelationsDTO(VehicleRDTO):
    category: Optional[VehicleCategoryRDTO] = None
    color: Optional[VehicleColorRDTO] = None
    owner: Optional[UserRDTO] = None
    organization: Optional[OrganizationRDTO] = None
    file: Optional[FileRDTO] = None

    class Config:
        from_attributes = True
