from typing import Optional

from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.adapters.dto.material.material_dto import MaterialCDTO, MaterialWithRelationsDTO
from app.adapters.repositories.material.material_repository import MaterialRepository
from app.adapters.repositories.workshop.workshop_repository import WorkshopRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel
from app.use_cases.base_case import BaseUseCase


class CreateMaterialCase(BaseUseCase[MaterialWithRelationsDTO]):

    def __init__(self, db: AsyncSession):
        self.repository = MaterialRepository(db)
        self.workshop_repository = WorkshopRepository(db)

    async def execute(
        self, dto: MaterialCDTO, file: Optional[FileModel] = None
    ) -> MaterialWithRelationsDTO:
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
                selectinload(self.repository.model.workshop),
            ],
        )
        return MaterialWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: MaterialCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[and_(func.lower(self.repository.model.sap_id) == dto.sap_id)]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"Запись с sap_id {dto.sap_id} уже существует."
            )
        existed_relations = await self.workshop_repository.get(dto.workshop_id)
        if not existed_relations:
            raise AppExceptionResponse.bad_request(
                message=f"Зависимость на цех с id {dto.workshop_id} не найдена."
            )
        dto.workshop_sap_id = existed_relations.sap_id
        return dto

    async def transform(self, dto: MaterialCDTO, file: FileModel) -> MaterialCDTO:
        dto.file_id = file.id
        return dto
