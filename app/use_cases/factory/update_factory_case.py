from typing import Optional

from fastapi import UploadFile
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.factory.factory_dto import (FactoryCDTO,
                                                  FactoryWithRelationsDTO)
from app.adapters.repositories.factory.factory_repository import \
    FactoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FactoryModel, FileModel
from app.infrastructure.services.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_cases.base_case import BaseUseCase


class UpdateFactoryCase(BaseUseCase[FactoryWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = FactoryRepository(db)
        self.service = FileService(db)

    async def execute(
        self, id: int, dto: FactoryCDTO, file: Optional[UploadFile]
    ) -> FactoryWithRelationsDTO:
        model = await self.validate(id=id, dto=dto)
        updated_dto = await self.transform(dto=dto, model=model, file=file)
        existed = await self.repository.update(obj=model, dto=updated_dto)
        existed = await self.repository.get(
            id=existed.id,
            options=self.repository.default_relationships(),
        )
        return FactoryWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: FactoryCDTO) -> FactoryModel:
        model = await self.repository.get(id=id)
        if model is None:
            raise AppExceptionResponse.not_found("Завод не найден")
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
                "Завод с таким SAP-ID уже существует"
            )
        return model

    async def transform(
        self, dto: FactoryCDTO, model: FactoryModel, file: Optional[UploadFile]
    ) -> FactoryCDTO:
        file_model = None
        if AppFileExtensionConstants.is_upload_file(file):
            if model.file_id:
                file_model = await self.service.update_file(
                    file_id=model.file_id,
                    new_file=file,
                    uploaded_folder=AppFileExtensionConstants.FactoryFolderName,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                )
            else:
                file_model = await self.service.save_file(
                    file=file,
                    uploaded_folder=AppFileExtensionConstants.FactoryFolderName,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                )
        if file_model:
            dto.file_id = file_model.id
        else:
            dto.file_id = model.file_id
        return dto
