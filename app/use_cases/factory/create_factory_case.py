from typing import Optional

from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.factory.factory_dto import (FactoryCDTO,
                                                  FactoryWithRelationsDTO)
from app.adapters.repositories.factory.factory_repository import \
    FactoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel
from app.use_cases.base_case import BaseUseCase


class CreateFactoryCase(BaseUseCase[FactoryWithRelationsDTO]):

    def __init__(self, db: AsyncSession):
        self.repository = FactoryRepository(db)

    async def execute(
        self, dto: FactoryCDTO, file: Optional[FileModel] = None
    ) -> FactoryWithRelationsDTO:
        await self.validate(dto=dto)
        if file:
            dto = await self.transform(dto=dto, file=file)
        existed = await self.repository.create(obj=self.repository.model(**dto.dict()))
        if not existed:
            raise AppExceptionResponse.bad_request(message=f"Что-то пошло не так")
        existed = await self.repository.get(
            id=existed.id,
            options=self.repository.default_relationships(),
        )
        return FactoryWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: FactoryCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[and_(func.lower(self.repository.model.sap_id) == dto.sap_id)]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"Запись с sap_id {dto.sap_id} уже существует."
            )

    async def transform(self, dto: FactoryCDTO, file: FileModel) -> FactoryCDTO:
        dto.file_id = file.id
        return dto
