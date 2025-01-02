from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_type.organization_type_dto import (
    OrganizationTypeRDTO,
)
from app.adapters.repositories.organization_type.organization_type_repository import (
    OrganizationTypeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrganizationTypeByValueCase(BaseUseCase[OrganizationTypeRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationTypeRepository(db)

    async def execute(self, value: str) -> OrganizationTypeRDTO:
        filters = [
            and_(
                func.lower(self.repository.model.value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(filters=filters)
        if not model:
            raise AppExceptionResponse.not_found("Тип организации не найден")
        return OrganizationTypeRDTO.from_orm(model)

    async def validate(self):
        pass
