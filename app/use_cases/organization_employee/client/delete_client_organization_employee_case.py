from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.services.file_service import FileService
from app.use_cases.base_case import BaseUseCase


class DeleteClientOrganizationEmployeeCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = OrganizationEmployeeRepository(db)
        self.service = FileService(db)

    async def execute(self, id: int, user: UserWithRelationsDTO) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int, user: UserWithRelationsDTO):
        organization_ids = [org.id for org in user.organizations]
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id == id,
                    or_(
                        self.repository.model.organization_id.in_(organization_ids),
                        self.repository.model.employee_id == user.id,
                    ),
                )
            ],
            options=self.repository.default_relationships(),
        )
        if existed is None:
            raise AppExceptionResponse.not_found(
                message="Организация-работник не найдена"
            )
