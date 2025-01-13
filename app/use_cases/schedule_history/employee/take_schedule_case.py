from datetime import datetime
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.schedule.schedule_dto import ScheduleCDTO
from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO, ScheduleHistoryCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.operation.operation_repository import OperationRepository
from app.adapters.repositories.schedule.schedule_repository import ScheduleRepository
from app.adapters.repositories.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ScheduleModel, OperationModel, ScheduleHistoryModel
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class TakeScheduleCase(BaseUseCase[ScheduleHistoryWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = ScheduleHistoryRepository(db)
        self.schedule_repository = ScheduleRepository(db)
        self.operation_repository = OperationRepository(db)
        #Global Variables
        self.schedule: Optional[ScheduleModel] = None
        self.operation: Optional[OperationModel] = None
        self.user: Optional[UserWithRelationsDTO] = None
        self.schedule_history: Optional[ScheduleHistoryModel] = None

    async def execute(
            self,
            schedule_id: int,
            user:UserWithRelationsDTO

    ) -> ScheduleHistoryWithRelationsDTO:
        self.user = user
        self.schedule = await self.schedule_repository.get(id=schedule_id,options=self.schedule_repository.default_relationships())
        self.operation = await self.operation_repository.get(id=self.schedule.current_operation_id if self.schedule else 0)
        await self.validate()
        await self.transform()
        self.schedule_history = await self.repository.get_with_filters(
            filters=[
                self.repository.model.schedule_id == self.schedule.id,
                self.repository.model.operation_id == self.operation.id,
                self.repository.model.is_passed is None,
                self.repository.model.responsible_id == user.id
            ],
            options=self.repository.default_relationships()
        )
        if not self.schedule_history:
            raise AppExceptionResponse.not_found("Расписание не найдено")
        return ScheduleHistoryWithRelationsDTO.from_orm(self.schedule_history)



    async def validate(self):
        if not self.schedule:
            raise AppExceptionResponse.bad_request(message="Расписание не найдено")

        if not self.schedule.is_active or self.schedule.is_canceled or self.schedule.is_executed or not self.schedule.current_operation_id:
            raise AppExceptionResponse.bad_request(message="Расписание не активно")

        if self.schedule.responsible_id or self.schedule.responsible_name:
            raise AppExceptionResponse.bad_request(message=f"Расписание уже присвоено оператору {self.schedule.responsible_name}")

        if not self.operation:
            raise AppExceptionResponse.bad_request(message="Операция не найдена")

        if self.operation.role_value != self.user.role.value:
            raise AppExceptionResponse.bad_request(message="Вы не имеете права изменять данные")

        if self.operation.value == AppDbValueConstants.ENTRY_CHECKPOINT:
            current_time = datetime.now()
            if current_time < self.schedule.start_at:
                raise AppExceptionResponse.bad_request(message="Время начала работы операции еще не наступило")
            if current_time > self.schedule.end_at:
                raise AppExceptionResponse.bad_request(message="Время начала работы операции уже прошло")

    async def transform(self):
        schedule_history = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.schedule_id == self.schedule.id,
                    self.repository.model.operation_id == self.operation.id,
                    self.repository.model.is_passed is None,
                    self.repository.model.responsible_id is None
                )
            ]
        )
        if schedule_history:
            schedule_history_cdto = ScheduleHistoryCDTO.from_orm(schedule_history)
            schedule_history_cdto.responsible_id = self.user.id
            schedule_history_cdto.responsible_name = self.user.name
            schedule_history_cdto.responsible_iin = self.user.iin
            self.schedule_history = await self.repository.update(obj=schedule_history,dto=schedule_history_cdto)
        else:
            schedule_history_cdto = ScheduleHistoryCDTO(
                schedule_id = self.schedule.id,
                operation_id = self.operation.id,
                responsible_id = self.user.id,
                responsible_name = self.user.name,
                responsible_iin = self.user.iin,
                is_passed = None,
                start_at = datetime.now(),
                end_at = None,
                canceled_at = None,
                cancel_reason = None
            )
            self.schedule_history = await self.repository.create(obj=self.repository.model(**schedule_history_cdto.dict()))
        if self.schedule_history:
            schedule_cdto = ScheduleCDTO.from_orm(self.schedule)
            schedule_cdto.responsible_id = self.schedule_history.responsible_id
            schedule_cdto.responsible_name = self.schedule_history.responsible_name
            schedule_cdto.is_used = True
            self.schedule = await self.schedule_repository.update(obj=self.schedule,dto=schedule_cdto)

