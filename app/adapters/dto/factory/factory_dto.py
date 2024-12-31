from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class FactoryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FactoryCDTO(BaseModel):
    file_id: DTOConstant.StandardNullableIntegerField()
    title: DTOConstant.StandardTextField()
    description: DTOConstant.StandardNullableTextField()
    sap_id: DTOConstant.StandardTextField()
    status: DTOConstant.StandardBooleanTrueField()

    class Config:
        from_attributes = True


class FactoryRDTO(FactoryDTO):
    file_id: DTOConstant.StandardNullableIntegerField()
    title: DTOConstant.StandardTextField()
    description: DTOConstant.StandardNullableTextField()
    sap_id: DTOConstant.StandardTextField()
    status: DTOConstant.StandardBooleanTrueField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class FactoryWithRelationsDTO(FactoryRDTO):
    file: Optional[FileRDTO] = None
