from typing import Optional, List

from app.adapters.dto.schedule_history.make_decision_dto import MakeDecisionDTO
from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO, UserRDTO
from app.adapters.repositories.operation.operation_repository import OperationRepository
from app.adapters.repositories.schedule.schedule_repository import ScheduleRepository
from app.adapters.repositories.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ScheduleModel, OperationModel, ScheduleHistoryModel, VehicleModel, OrganizationModel, \
    OrderModel
from app.use_cases.base_case import BaseUseCase
from sqlalchemy.ext.asyncio import AsyncSession


class MakeDecisionCase(BaseUseCase[ScheduleHistoryWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = ScheduleHistoryRepository(db)
        self.schedule_repository = ScheduleRepository(db)
        self.operation_repository = OperationRepository(db)
        # Global Variables
        self.schedule: Optional[ScheduleModel] = None
        self.vehicle: Optional[VehicleModel] = None
        self.trailer: Optional[VehicleModel] = None
        self.organization: Optional[OrganizationModel] = None
        self.driver: Optional[UserRDTO] = None
        self.owner: Optional[UserRDTO] = None
        self.order: Optional[OrderModel] = None
        self.operations: List[OperationModel] = []
        self.current_operation: Optional[OperationModel] = None
        self.employee: Optional[UserWithRelationsDTO] = None
        self.schedule_history: Optional[ScheduleHistoryModel] = None
        self.dto:Optional[MakeDecisionDTO] = None

    async def execute(
            self,
            schedule_id:int,
            dto:MakeDecisionDTO,
            employee: UserWithRelationsDTO
    ) -> ScheduleHistoryWithRelationsDTO:
        self.dto = dto
        self.employee = employee
        self.schedule = await self.schedule_repository.get(
            id=schedule_id,
            options=self.schedule_repository.default_relationships()
        )
        self.operations = await self.operation_repository.get_all(
            options=self.operation_repository.default_relationships()
        )
        await self.validate()
        await self.transform()

    async def validate(self):
        if not self.schedule:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        if not self.schedule.is_active:
            raise AppExceptionResponse.bad_request("Расписание не активно")
        if not self.schedule.vehicle:
            raise AppExceptionResponse.bad_request("Не указан автомобиль в расписании")
        if not self.schedule.order:
            raise AppExceptionResponse.bad_request("Не указан заказ в расписании")
        if not self.schedule.driver:
            raise AppExceptionResponse.bad_request("Не указан водитель")
        if not self.schedule.current_operation:
            raise AppExceptionResponse.bad_request("Не указана текущая операция")
        if self.schedule.organization_bin:
            if not self.schedule.organization:
                raise AppExceptionResponse.bad_request("Не указана организация")
        if self.schedule.current_operation.role_id != None:
            if not self.schedule.responsible:
                raise AppExceptionResponse.bad_request("Сначала надо взять под отвественность данный этап")
            if self.schedule.current_operation.role_value != self.employee.role.keycloak_value:
                raise AppExceptionResponse.forbidden(message="Вы не имеете права применять решения по данному расписанию")


    async def transform(self):
        self.vehicle = self.schedule.vehicle
        self.trailer = self.schedule.trailer
        self.organization = self.schedule.organization
        self.driver = self.schedule.driver
        self.owner = self.schedule.owner
        self.order = self.schedule.order
        self.current_operation = self.schedule.current_operation



