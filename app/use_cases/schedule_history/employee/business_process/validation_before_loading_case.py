from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.schedule_history.make_decision_dto import MakeDecisionDTO
from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO, ScheduleHistoryCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ScheduleModel, OperationModel, ScheduleHistoryModel
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase
from app.use_cases.schedule_history.employee.take_schedule_case import TakeScheduleCase


class ValidationBeforeLoadingCase(BaseUseCase[ScheduleHistoryWithRelationsDTO]):

    def __init__(self, db: AsyncSession):
        self.schedule_history_repository = ScheduleHistoryRepository(db)
        self.take_schedule_use_case = TakeScheduleCase(db)
        self.dto: Optional[MakeDecisionDTO] = None
        self.schedule: Optional[ScheduleModel] = None
        self.employee: Optional[UserWithRelationsDTO] = None
        self.operations: List[OperationModel] = []
        self.current_operation: Optional[OperationModel] = None
        self.schedule_history: Optional[ScheduleHistoryModel] = None

    async def execute(
        self,
        dto: MakeDecisionDTO,
        schedule: ScheduleModel,
        employee: UserWithRelationsDTO,
        operations: List[OperationModel],
    ) -> ScheduleHistoryModel:
        self.schedule = schedule
        self.employee = employee
        self.dto = dto
        self.operations = operations

        # Определяем текущую операцию
        self.current_operation = next(
            (op for op in operations if op.value == AppDbValueConstants.VALIDATION_BEFORE_LOADING),
            None
        )

        await self.validate()
        return await self.transform()

    async def validate(self):
        # Проверка на соответствие операции
        if not self.current_operation:
            raise AppExceptionResponse.bad_request("Текущая операция не найдена")
        if self.schedule.current_operation_value != AppDbValueConstants.VALIDATION_BEFORE_LOADING:
            raise AppExceptionResponse.bad_request("Расписание не соответствует текущей операции")

        # Проверка прав пользователя
        if self.employee.role.keycloak_value != self.current_operation.role_value or self.schedule.responsible_id != self.employee.id:
            raise AppExceptionResponse.forbidden("Вы не имеете права принимать решения по данному процессу")

        # Проверка веса тары
        if self.dto.is_passed and not self.dto.vehicle_tara_t:
            raise AppExceptionResponse.bad_request("Введите вес тары транспортного средства")

    async def transform(self) -> ScheduleHistoryModel:
        current_datetime = datetime.now()

        # Получаем или создаём запись в истории
        schedule_history = await self._get_or_create_schedule_history()

        # Обновляем данные истории
        schedule_history_dto = self._prepare_schedule_history_update(schedule_history, current_datetime)
        await self.schedule_history_repository.update(obj=schedule_history, dto=schedule_history_dto)


        # Возвращаем обновлённую запись истории
        return await self._get_actual_schedule_history()

    async def _get_or_create_schedule_history(self) -> ScheduleHistoryModel:
        schedule_history = await self._get_actual_schedule_history()

        if not schedule_history:
            # Если история отсутствует, создаём её через `TakeScheduleCase`
            await self.take_schedule_use_case.execute(schedule_id=self.schedule.id, user=self.employee)
            schedule_history = await self._get_actual_schedule_history()

        if not schedule_history:
            raise AppExceptionResponse.internal_error("Не удалось создать или найти запись истории")
        return schedule_history

    async def _get_actual_schedule_history(self) -> Optional[ScheduleHistoryModel]:
        return await self.schedule_history_repository.get_first_with_filters(
            filters=[
                and_(
                    self.schedule_history_repository.model.schedule_id == self.schedule.id,
                    self.schedule_history_repository.model.operation_id == self.current_operation.id,
                    self.schedule_history_repository.model.responsible_id == self.employee.id,
                    self.schedule_history_repository.model.is_passed.is_(None)
                )
            ],
            options=self.schedule_history_repository.default_relationships()
        )

    def _prepare_schedule_history_update(
        self, schedule_history: ScheduleHistoryModel, current_datetime: datetime
    ) -> ScheduleHistoryCDTO:
        # Обновление истории с учётом DTO
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.is_passed = self.dto.is_passed
        schedule_history_dto.canceled_at = current_datetime if not self.dto.is_passed else None
        schedule_history_dto.cancel_reason = self.dto.cancel_reason if not self.dto.is_passed else None
        schedule_history_dto.end_at = current_datetime
        return schedule_history_dto

