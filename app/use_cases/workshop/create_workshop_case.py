from typing import Optional

from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.workshop.workshop_dto import (
    WorkshopCDTO,
    WorkshopWithRelationsDTO,
)
from app.adapters.repositories.factory.factory_repository import FactoryRepository
from app.adapters.repositories.workshop.workshop_repository import WorkshopRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel
from app.use_cases.base_case import BaseUseCase


class CreateWorkshopCase(BaseUseCase[WorkshopWithRelationsDTO]):

    def __init__(self, db: AsyncSession):
        self.repository = WorkshopRepository(db)
        self.factory_repository = FactoryRepository(db)

    async def execute(
        self, dto: WorkshopCDTO, file: Optional[FileModel] = None
    ) -> WorkshopWithRelationsDTO:
        dto = await self.validate(dto=dto)
        if file:
            dto = await self.transform(dto=dto, file=file)
        existed = await self.repository.create(obj=self.repository.model(**dto.dict()))
        if not existed:
            raise AppExceptionResponse.bad_request(message=f"Что-то пошло не так")
        existed = await self.repository.get(
            id=existed.id,
            options=[
                selectinload(self.repository.model.file),
                selectinload(self.repository.model.factory),
            ],
        )
        return WorkshopWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: WorkshopCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[and_(func.lower(self.repository.model.sap_id) == dto.sap_id)]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"Запись с sap_id {dto.sap_id} уже существует."
            )
        existed_relations = await self.factory_repository.get(dto.factory_id)
        if not existed_relations:
            raise AppExceptionResponse.bad_request(
                message=f"Зависимость на завод с id {dto.factory_id} не найдена."
            )
        dto.factory_sap_id = existed_relations.sap_id
        return dto

    async def transform(self, dto: WorkshopCDTO, file: FileModel) -> WorkshopCDTO:
        dto.file_id = file.id
        return dto
