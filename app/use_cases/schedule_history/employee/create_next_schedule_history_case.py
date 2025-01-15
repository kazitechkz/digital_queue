from datetime import datetime
from typing import Optional
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO, ScheduleHistoryCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.base_weight.base_weight_repository import BaseWeightRepository
from app.adapters.repositories.operation.operation_repository import OperationRepository
from app.adapters.repositories.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OperationModel, ScheduleModel, ScheduleHistoryModel
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CreateNextScheduleHistoryCase(BaseUseCase[ScheduleHistoryModel]):
    def __init__(self, db: AsyncSession):
        self.operation_repository = OperationRepository(db)
        self.schedule_history_repository = ScheduleHistoryRepository(db)
        self.base_weight_repository = BaseWeightRepository(db)
        #Variables
        self.current_operation:Optional[OperationModel] = None
        self.schedule: Optional[ScheduleModel] = None
        self.employee: Optional[UserWithRelationsDTO] = None

    async def execute(
            self,
            current_operation: OperationModel,
    ) -> ScheduleHistoryModel:
        self.current_operation = current_operation
        await self.validate()
        return await self.transform()

    async def validate(self):
        if not self.current_operation:
            raise AppExceptionResponse.bad_request("Операции не существует")

    async def transform(self):
        current_datetime = datetime.now()
        next_operation = await self.operation_repository.next_operation(self.current_operation.next_id)

        # Обработка случая INITIAL_WEIGHING
        if next_operation.value == AppDbValueConstants.INITIAL_WEIGHING:
            existed_base_weighting = await self._check_base_weighting(current_datetime)
            if existed_base_weighting:
                schedule_history_cdto = self._create_schedule_history(
                    next_operation=next_operation,
                    is_passed=True,
                    start_at=current_datetime,
                    end_at=current_datetime
                )
                next_operation = await self.operation_repository.next_operation(next_operation.next_id)
            else:
                schedule_history_cdto = await self._create_empty_schedule_history(next_operation)
        else:
            schedule_history_cdto = await self._create_empty_schedule_history(next_operation)

        return await self.schedule_history_repository.create(
            obj=self.schedule_history_repository.model(**schedule_history_cdto.dict())
        )

    async def _check_base_weighting(self, current_datetime):
        """
        Проверяет существование взвешивания по номеру машины и времени.
        """
        return await self.base_weight_repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.base_weight_repository.model.car_number) == self.schedule.car_number.lower(),
                    self.base_weight_repository.model.measured_to >= current_datetime
                )
            ]
        )

    def _create_schedule_history(self, next_operation, is_passed, start_at, end_at, cancel_reason=None):
        """
        Создает DTO для истории расписания.
        """
        return ScheduleHistoryCDTO(
            schedule_id=self.schedule.id,
            operation_id=next_operation.id,
            responsible_id=self.employee.id if is_passed else None,
            responsible_name=self.employee.name if is_passed else None,
            responsible_iin=self.employee.iin if is_passed else None,
            is_passed=is_passed,
            start_at=start_at,
            end_at=end_at,
            canceled_at=start_at if not is_passed and cancel_reason else None,
            cancel_reason=cancel_reason
        )

    async def _create_empty_schedule_history(self, next_operation):
        """
        Создает пустую запись в истории расписания в зависимости от этапа.
        """
        current_datetime = datetime.now()
        if next_operation.is_last:
            if next_operation.value == AppDbValueConstants.SUCCESSFULLY_COMPLETED:
                return self._create_schedule_history(
                    next_operation=next_operation,
                    is_passed=True,
                    start_at=current_datetime,
                    end_at=current_datetime
                )
            elif next_operation.value == AppDbValueConstants.CANCELLED:
                return self._create_schedule_history(
                    next_operation=next_operation,
                    is_passed=False,
                    start_at=current_datetime,
                    end_at=current_datetime,
                    cancel_reason="Предыдущая операция была отменена"
                )
        # Для промежуточных операций
        return ScheduleHistoryCDTO(
            schedule_id=self.schedule.id,
            operation_id=next_operation.id,
            responsible_id=None,
            responsible_name=None,
            responsible_iin=None,
            is_passed=None,
            start_at=None,
            end_at=None,
            canceled_at=None,
            cancel_reason=None
        )
