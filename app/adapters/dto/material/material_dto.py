from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.workshop.workshop_dto import WorkshopRDTO
from app.shared.dto_constants import DTOConstant


class MaterialDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class MaterialCDTO(BaseModel):
    file_id: DTOConstant.StandardNullableIntegerField()
    workshop_id: DTOConstant.StandardIntegerField()
    title: DTOConstant.StandardTextField()
    description: DTOConstant.StandardNullableTextField()
    sap_id: DTOConstant.StandardVarcharField()
    workshop_sap_id: DTOConstant.StandardVarcharField()
    status: DTOConstant.StandardBooleanTrueField()
    price_without_taxes: DTOConstant.StandardPriceField()
    price_with_taxes: DTOConstant.StandardPriceField()
    class Config:
        from_attributes = True


class MaterialRDTO(MaterialDTO):
    file_id: DTOConstant.StandardNullableIntegerField()
    workshop_id: DTOConstant.StandardNullableIntegerField()
    title: DTOConstant.StandardTextField()
    description: DTOConstant.StandardNullableTextField()
    sap_id: DTOConstant.StandardVarcharField()
    workshop_sap_id: DTOConstant.StandardVarcharField()
    status: DTOConstant.StandardBooleanTrueField()
    price_without_taxes: DTOConstant.StandardPriceField()
    price_with_taxes: DTOConstant.StandardPriceField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class MaterialWithRelationsDTO(MaterialRDTO):
    file: Optional[FileRDTO] = None
    workshop: Optional[WorkshopRDTO] = None

    class Config:
        from_attributes = True