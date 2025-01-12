from typing import Optional

from fastapi import UploadFile
from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_employee.organization_employee_dto import (
    OrganizationEmployeeCDTO, OrganizationEmployeeWithRelationsDTO)
from app.adapters.repositories.organization.organization_repository import \
    OrganizationRepository
from app.adapters.repositories.organization_employee.organization_employee_repository import \
    OrganizationEmployeeRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class UpdateOrganizationEmployeeCase(BaseUseCase[OrganizationEmployeeWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationEmployeeRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(
        self, id: int, dto: OrganizationEmployeeCDTO
    ) -> OrganizationEmployeeWithRelationsDTO:
        model = await self.repository.get(id=id)
        if not model:
            raise AppExceptionResponse().bad_request(
                message="Организация-работник не найдена"
            )
        dto = await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=model, dto=dto)
        if not model:
            raise AppExceptionResponse().internal_error(
                message="Произошла ошибка при обновлении организации-работник"
            )
        model = await self.repository.get(
            id=model.id,
            options=self.repository.default_relationships(),
        )
        return OrganizationEmployeeWithRelationsDTO.from_orm(model)

    async def validate(self, id: id, dto: OrganizationEmployeeCDTO):
        user = await self.user_repository.get_first_with_filters(
            filters=[and_(self.user_repository.model.id == dto.employee_id)],
            options=self.user_repository.default_relationships(),
        )
        if not user:
            raise AppExceptionResponse().bad_request(
                message="Указанный работник организации не найден"
            )
        if user.user_type.value != AppDbValueConstants.INDIVIDUAL_VALUE:
            raise AppExceptionResponse().bad_request(
                message="Работник организации должен быть физ. лицом"
            )

        organization = await self.organization_repository.get(id=dto.organization_id)
        if not organization:
            raise AppExceptionResponse().bad_request(message="Организация не найдена")
        existed_organization_employee = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.organization_id == dto.organization_id,
                    self.repository.model.employee_id == dto.employee_id,
                    self.repository.model.id != id,
                )
            ]
        )
        if existed_organization_employee:
            raise AppExceptionResponse().bad_request(
                message="Данный работник уже работает на организацию"
            )

        dto.bin = organization.bin
        dto.sid = user.sid
        return dto
