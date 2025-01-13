from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_employee.organization_employee_dto import (
    OrganizationEmployeeWithRelationsDTO,
)
from app.adapters.repositories.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrganizationEmployeeByValueCase(
    BaseUseCase[OrganizationEmployeeWithRelationsDTO]
):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationEmployeeRepository(db)

    async def execute(self, value: str) -> OrganizationEmployeeWithRelationsDTO:
        filters = [
            or_(
                func.lower(self.repository.model.bin) == value.lower(),
                func.lower(self.repository.model.sid) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Организация-Работник не найдено")
        return OrganizationEmployeeWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
