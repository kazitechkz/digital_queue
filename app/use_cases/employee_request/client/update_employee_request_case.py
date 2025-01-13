from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.employee_request.employee_request_dto import (
    EmployeeRequestClientCDTO,
    EmployeeRequestOwnerCDTO,
    EmployeeRequestWithRelationsDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.employee_request.employee_request_repository import (
    EmployeeRequestRepository,
)
from app.adapters.repositories.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import EmployeeRequestModel
from app.use_cases.base_case import BaseUseCase


class UpdateEmployeeRequestCase(BaseUseCase[EmployeeRequestWithRelationsDTO]):

    def __init__(self, db: AsyncSession):
        self.repository = EmployeeRequestRepository(db)
        self.organization_employee_repository = OrganizationEmployeeRepository(db)

    async def execute(
        self, id: int, dto: EmployeeRequestClientCDTO, user: UserWithRelationsDTO
    ) -> EmployeeRequestWithRelationsDTO:
        model: EmployeeRequestModel = await self.validate(id=id, dto=dto, user=user)
        existed_organization_employee = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.organization_employee_repository.model.employee_id
                    == model.employee_id,
                    self.organization_employee_repository.model.organization_id
                    == model.organization_id,
                )
            ]
        )
        if not existed_organization_employee and dto.status == 1:
            await self.organization_employee_repository.create(
                obj=self.organization_employee_repository.model(
                    employee_id=user.id,
                    organization_id=model.organization_id,
                    bin=model.organization_bin,
                    sid=user.sid,
                    request_id=model.id,
                )
            )
        model = await self.repository.update(obj=model, dto=dto)
        if not model:
            raise AppExceptionResponse().internal_error(
                message="Произошла ошибка при обновлении заявки на работу"
            )
        model = await self.repository.get(
            id=model.id,
            options=self.repository.default_relationships(),
        )
        return EmployeeRequestWithRelationsDTO.from_orm(model)

    async def validate(
        self, id: int, dto: EmployeeRequestOwnerCDTO, user: UserWithRelationsDTO
    ):
        model = await self.repository.get(id=id)
        if not model:
            raise AppExceptionResponse.not_found("Заявка на работу не найдена")

        if model.employee_id != user.id:
            raise AppExceptionResponse.bad_request(
                "Вы не можете оставить ответ на данную заявку"
            )

        if model.status != 0:
            raise AppExceptionResponse.bad_request("Заявка на работу уже отвечена")
        return model
