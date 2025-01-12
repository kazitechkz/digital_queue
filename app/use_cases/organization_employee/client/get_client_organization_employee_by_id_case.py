from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_employee.organization_employee_dto import \
    OrganizationEmployeeWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.organization_employee.organization_employee_repository import \
    OrganizationEmployeeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetClientOrganizationEmployeeByIdCase(
    BaseUseCase[OrganizationEmployeeWithRelationsDTO]
):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationEmployeeRepository(db)

    async def execute(self, id: int,user:UserWithRelationsDTO) -> OrganizationEmployeeWithRelationsDTO:
        organization_ids = [org.id for org in user.organizations]
        model = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id == id,
                    or_(
                        self.repository.model.organization_id.in_(organization_ids),
                        self.repository.model.employee_id == user.id,
                    )
                )
            ],
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Организация-Работник не найдена")
        return OrganizationEmployeeWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
