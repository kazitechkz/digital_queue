from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_employee.organization_employee_dto import OrganizationEmployeeWithRelationsDTO
from app.adapters.repositories.organization_employee.organization_employee_repository import \
    OrganizationEmployeeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrganizationEmployeeByIdCase(BaseUseCase[OrganizationEmployeeWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationEmployeeRepository(db)

    async def execute(self, id: int) -> OrganizationEmployeeWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Организация-Работник не найдена")
        return OrganizationEmployeeWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
