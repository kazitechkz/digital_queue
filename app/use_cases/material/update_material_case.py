from typing import Optional

from fastapi import UploadFile
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.material.material_dto import (
    MaterialCDTO,
    MaterialWithRelationsDTO,
)
from app.adapters.repositories.material.material_repository import MaterialRepository
from app.adapters.repositories.workshop.workshop_repository import WorkshopRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import MaterialModel
from app.infrastructure.services.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_cases.base_case import BaseUseCase


class UpdateMaterialCase(BaseUseCase[MaterialWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = MaterialRepository(db)
        self.service = FileService(db)
        self.workshop_repository = WorkshopRepository(db)

    async def execute(
        self, id: int, dto: MaterialCDTO, file: Optional[UploadFile]
    ) -> MaterialWithRelationsDTO:
        model = await self.validate(id=id, dto=dto)
        updated_dto = await self.transform(dto=dto, model=model, file=file)
        existed = await self.repository.update(obj=model, dto=updated_dto)
        existed = await self.repository.get(
            id=existed.id,
            options=self.repository.default_relationships(),
        )
        return MaterialWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: MaterialCDTO) -> MaterialModel:
        model = await self.repository.get(id=id)
        if model is None:
            raise AppExceptionResponse.not_found("Материал не найден")
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.repository.model.sap_id) == dto.sap_id.lower(),
                    self.repository.model.id != id,
                )
            ]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Материал с таким SAP-ID уже существует"
            )
        existed_workshop = await self.workshop_repository.get(id=dto.workshop_id)
        if not existed_workshop:
            raise AppExceptionResponse.bad_request("Цех не найден")
        return model

    async def transform(
        self, dto: MaterialCDTO, model: MaterialModel, file: Optional[UploadFile]
    ) -> MaterialCDTO:
        file_model = None
        if AppFileExtensionConstants.is_upload_file(file):
            if model.file_id:
                file_model = await self.service.update_file(
                    file_id=model.file_id,
                    new_file=file,
                    uploaded_folder=AppFileExtensionConstants.MaterialFolderName,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                )
            else:
                file_model = await self.service.save_file(
                    file=file,
                    uploaded_folder=AppFileExtensionConstants.MaterialFolderName,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                )
        if file_model is not None:
            dto.file_id = file_model.id
        else:
            dto.file_id = model.file_id
        existed_workshop = await self.workshop_repository.get(id=dto.workshop_id)
        if existed_workshop:
            dto.workshop_sap_id = existed_workshop.sap_id
        return dto
