import datetime
from typing import Optional, List
from app.adapters.dto.schedule.schedule_dto import ScheduleCDTO, ScheduleRDTO
from app.adapters.dto.schedule_history.make_decision_dto import MakeDecisionDTO
from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO, UserRDTO
from app.adapters.repositories.operation.operation_repository import OperationRepository
from app.adapters.repositories.schedule.schedule_repository import ScheduleRepository
from app.adapters.repositories.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ScheduleModel, OperationModel, ScheduleHistoryModel, VehicleModel, OrganizationModel, \
    OrderModel
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase
from sqlalchemy.ext.asyncio import AsyncSession
from app.use_cases.schedule_history.employee.business_process.entry_checkpoint_case import EntryCheckPointCase
from app.use_cases.schedule_history.employee.business_process.initial_weighting_case import InitialWeightingCase
from app.use_cases.schedule_history.employee.business_process.loading_goods_case import LoadingGoodsCase
from app.use_cases.schedule_history.employee.business_process.validation_before_loading_case import \
    ValidationBeforeLoadingCase
from app.use_cases.schedule_history.employee.create_next_schedule_history_case import CreateNextScheduleHistoryCase


class MakeDecisionCase(BaseUseCase[ScheduleHistoryWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ScheduleHistoryRepository(db)
        self.schedule_repository = ScheduleRepository(db)
        self.operation_repository = OperationRepository(db)
        self.create_next_schedule_history_case = CreateNextScheduleHistoryCase(db)
        self.employee: Optional[UserWithRelationsDTO] = None
        self.dto: Optional[MakeDecisionDTO] = None
        # State
        self.schedule: Optional[ScheduleModel] = None
        self.current_operation: Optional[OperationModel] = None
        self.next_operation: Optional[OperationModel] = None
        self.schedule_history: Optional[ScheduleHistoryModel] = None

    async def execute(
            self,
            schedule_id: int,
            dto: MakeDecisionDTO,
            employee: UserWithRelationsDTO
    ) -> ScheduleHistoryWithRelationsDTO:
        self.dto = dto
        self.employee = employee
        self.schedule = await self._get_schedule(schedule_id)
        await self.validate()
        await self.transform()
        await self._call_operation_process()
        await self._update_schedule()
        if not self.schedule_history:
            raise AppExceptionResponse.bad_request("Не удалось создать историю расписания")
        return ScheduleHistoryWithRelationsDTO.from_orm(self.schedule_history)

    async def _get_schedule(self, schedule_id: int) -> ScheduleModel:
        schedule = await self.schedule_repository.get(
            id=schedule_id,
            options=self.schedule_repository.default_relationships()
        )
        if not schedule:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        return schedule

    async def validate(self):
        if not self.schedule.is_active:
            raise AppExceptionResponse.bad_request("Расписание не активно")
        if self.schedule.is_executed:
            raise AppExceptionResponse.bad_request("Расписание уже выполнено")
        if self.schedule.is_canceled:
            raise AppExceptionResponse.bad_request("Расписание отменено")
        if not self.schedule.vehicle:
            raise AppExceptionResponse.bad_request("Не указан автомобиль в расписании")
        if not self.schedule.order:
            raise AppExceptionResponse.bad_request("Не указан заказ в расписании")
        if self.schedule.organization_bin and not self.schedule.organization:
            raise AppExceptionResponse.bad_request("Не указана организация")
        if self.schedule.current_operation.role_id:
            if not self.schedule.responsible:
                raise AppExceptionResponse.bad_request("Этап требует ответственного")
            if self.schedule.current_operation.role_value != self.employee.role.keycloak_value:
                raise AppExceptionResponse.forbidden(message="У вас нет прав для принятия решения")

    async def transform(self):
        self.current_operation = self.schedule.current_operation
        if not self.current_operation.is_last:
            self.next_operation = await self.operation_repository.next_operation(self.current_operation.id)
        if not self.current_operation.can_cancel:
            self.dto.is_passed = True

    async def _call_operation_process(self):
        operation_dispatcher = {
            AppDbValueConstants.ENTRY_CHECKPOINT: EntryCheckPointCase,
            AppDbValueConstants.INITIAL_WEIGHING: InitialWeightingCase,
            AppDbValueConstants.VALIDATION_BEFORE_LOADING: ValidationBeforeLoadingCase,
            AppDbValueConstants.LOADING_GOODS:LoadingGoodsCase,
        }
        use_case_class = operation_dispatcher.get(self.current_operation.value)
        if not use_case_class:
            raise AppExceptionResponse.bad_request(f"Операция с кодом {self.current_operation.value} не найдена")
        use_case = use_case_class(self.db)
        self.schedule_history = await use_case.execute(
            dto=self.dto,
            schedule=self.schedule,
            employee=self.employee
        )

    async def _update_schedule(self):
        if not self.schedule_history:
            raise AppExceptionResponse.internal_error("История расписания не найдена")

        dto = ScheduleRDTO.from_orm(self.schedule)
        if self.schedule_history.is_passed:
            dto = await self._handle_next_operation(dto)
        else:
            dto = self._cancel_schedule(dto)
        self.schedule = await self.schedule_repository.update(obj=self.schedule, dto=dto)

    async def _handle_next_operation(self, dto: ScheduleRDTO) -> ScheduleRDTO:
        if not self.next_operation:
            return dto

        dto.current_operation_id = self.next_operation.id
        dto.current_operation_name = self.next_operation.title
        dto.current_operation_value = self.next_operation.value

        if self.next_operation.is_last:
            if self.next_operation.value == AppDbValueConstants.SUCCESSFULLY_COMPLETED:
                return self._end_schedule(dto)
            elif self.next_operation.value == AppDbValueConstants.CANCELLED:
                return self._cancel_schedule(dto)
        return dto

    def _end_schedule(self, dto: ScheduleRDTO) -> ScheduleRDTO:
        dto.end_at = datetime.datetime.now()
        dto.is_executed = True
        dto.is_active = False
        dto.is_canceled = False
        return dto

    def _cancel_schedule(self, dto: ScheduleRDTO) -> ScheduleRDTO:
        dto.end_at = datetime.datetime.now()
        dto.is_executed = False
        dto.is_active = False
        dto.is_canceled = True
        dto.cancel_reason = "Процесс отменён"
        return dto


