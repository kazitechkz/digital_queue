from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.factory.factory_dto import FactoryRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class WorkshopDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class WorkshopCDTO(BaseModel):
    file_id: DTOConstant.StandardNullableIntegerField()
    factory_id: DTOConstant.StandardIntegerField()
    title: DTOConstant.StandardTextField()
    description: DTOConstant.StandardNullableTextField()
    sap_id: DTOConstant.StandardVarcharField()
    factory_sap_id: DTOConstant.StandardVarcharField()
    status: DTOConstant.StandardBooleanTrueField()

    class Config:
        from_attributes = True


class WorkshopRDTO(WorkshopDTO):
    file_id: DTOConstant.StandardNullableIntegerField()
    factory_id: DTOConstant.StandardNullableIntegerField()
    title: DTOConstant.StandardTextField()
    description: DTOConstant.StandardNullableTextField()
    sap_id: DTOConstant.StandardVarcharField()
    factory_sap_id: DTOConstant.StandardVarcharField()
    status: DTOConstant.StandardBooleanTrueField()

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class WorkshopWithRelationsDTO(WorkshopRDTO):
    file: Optional[FileRDTO] = None
    factory: Optional[FactoryRDTO] = None

    class Config:
        from_attributes = True
