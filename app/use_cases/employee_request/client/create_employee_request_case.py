from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.employee_request.employee_request_dto import (
    EmployeeRequestCDTO,
    EmployeeRequestOwnerCDTO,
    EmployeeRequestWithRelationsDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.employee_request.employee_request_repository import (
    EmployeeRequestRepository,
)
from app.adapters.repositories.organization.organization_repository import (
    OrganizationRepository,
)
from app.adapters.repositories.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CreateEmployeeRequestCase(BaseUseCase[EmployeeRequestWithRelationsDTO]):

    def __init__(self, db: AsyncSession):
        self.repository = EmployeeRequestRepository(db)
        self.organization_employee_repository = OrganizationEmployeeRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(
        self, dto: EmployeeRequestOwnerCDTO, user: UserWithRelationsDTO
    ) -> EmployeeRequestWithRelationsDTO:
        dto_dict: dict = await self.validate(dto=dto, user=user)
        model = await self.repository.create(obj=self.repository.model(**dto_dict))
        if not model:
            raise AppExceptionResponse().internal_error(
                message="Ошибка создания заявки на сотрудника"
            )
        model = await self.repository.get(
            id=model.id, options=self.repository.default_relationships()
        )
        return EmployeeRequestWithRelationsDTO.from_orm(model)

    async def validate(self, dto: EmployeeRequestOwnerCDTO, user: UserWithRelationsDTO):
        existed_employee = await self.user_repository.get_first_with_filters(
            filters=[
                and_(
                    self.user_repository.model.id == dto.employee_id,
                )
            ],
            options=self.user_repository.default_relationships(),
        )
        if not existed_employee:
            raise AppExceptionResponse().bad_request(message="Работник не найден")

        existed_organization_employee = (
            await self.organization_employee_repository.get_first_with_filters(
                filters=[
                    and_(
                        self.organization_employee_repository.model.employee_id
                        == dto.employee_id,
                        self.organization_employee_repository.model.organization_id
                        == dto.organization_id,
                    )
                ],
                options=self.organization_employee_repository.default_relationships(),
            )
        )
        if existed_organization_employee:
            raise AppExceptionResponse().bad_request(
                message="Работник уже является сотрудником организации"
            )
        organization = await self.organization_repository.get_first_with_filters(
            filters=[
                and_(
                    self.organization_repository.model.id == dto.organization_id,
                    self.organization_repository.model.owner_id == user.id,
                )
            ],
            options=self.user_repository.default_relationships(),
        )
        if not organization:
            raise AppExceptionResponse().bad_request(
                message="Организация не найдена или у владельца нет доступа"
            )
        if not existed_employee.user_type:
            raise AppExceptionResponse().bad_request(
                message="Работник должен быть физ. лицом"
            )
        if existed_employee.user_type.value != AppDbValueConstants.INDIVIDUAL_VALUE:
            raise AppExceptionResponse().bad_request(
                message="Работник должен быть физ. лицом"
            )

        dto_dict = await self.transform(
            dto=dto, organization=organization, employee=existed_employee, owner=user
        )
        return dto_dict

    async def transform(
        self, dto: EmployeeRequestOwnerCDTO, organization, employee, owner
    ) -> dict:
        return {
            "organization_id": organization.id,
            "organization_full_name": organization.full_name,
            "organization_bin": organization.bin,
            "owner_id": owner.id,
            "owner_name": owner.name,
            "owner_sid": owner.sid,
            "employee_id": employee.id,
            "employee_name": employee.name,
            "employee_email": employee.email,
            "employee_sid": employee.sid,
            "status": 0,
            "requested_at": datetime.now,
            "decided_at": None,
        }
