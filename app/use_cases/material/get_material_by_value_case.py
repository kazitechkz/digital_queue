from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.material.material_dto import MaterialWithRelationsDTO
from app.adapters.repositories.material.material_repository import \
    MaterialRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetMaterialByValueCase(BaseUseCase[MaterialWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = MaterialRepository(db)

    async def execute(self, value: str) -> MaterialWithRelationsDTO:
        filters = [
            and_(
                func.lower(self.repository.model.sap_id) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Материал не найден")
        return MaterialWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
