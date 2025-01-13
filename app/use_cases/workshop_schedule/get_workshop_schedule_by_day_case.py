from datetime import date, datetime, time, timedelta
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_by_day_dto import (
    WorkshopScheduleByDayDTO,
)
from app.adapters.dto.workshop_schedule.workshop_schedule_space_dto import (
    WorkshopScheduleSpaceDTO,
)
from app.adapters.repositories.schedule.schedule_repository import ScheduleRepository
from app.adapters.repositories.workshop.workshop_repository import WorkshopRepository
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import WorkshopModel, WorkshopScheduleModel
from app.use_cases.base_case import BaseUseCase


class GetWorkshopScheduleByDayCase(BaseUseCase[list[WorkshopScheduleSpaceDTO]]):

    def __init__(self, db: AsyncSession):
        self.repository = WorkshopScheduleRepository(db)
        self.workshop_repository = WorkshopRepository(db)
        self.schedule_repository = ScheduleRepository(db)

    async def execute(
        self, dto: WorkshopScheduleByDayDTO
    ) -> list[WorkshopScheduleByDayDTO]:
        workshop = await self.workshop_repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.workshop_repository.model.sap_id)
                    == dto.workshop_sap_id.lower(),
                    self.workshop_repository.model.status == True,
                )
            ]
        )
        active_workshop_schedule = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.repository.model.workshop_sap_id)
                    == dto.workshop_sap_id.lower(),
                    self.repository.model.is_active == True,
                    # func.DATE(self.repository.model.start_at) <= dto.schedule_date,
                    # func.DATE(self.repository.model.end_at) >= dto.schedule_date,
                )
            ]
        )
        if not active_workshop_schedule:
            return []
        await self.validate(
            dto=dto,
            workshop=workshop,
            active_workshop_schedule=active_workshop_schedule,
        )
        return await self.transform(
            dto=dto, active_workshop_schedule=active_workshop_schedule
        )

    async def validate(
        self,
        dto: WorkshopScheduleByDayDTO,
        workshop: Optional[WorkshopModel],
        active_workshop_schedule: WorkshopScheduleModel,
    ):
        if not workshop:
            raise AppExceptionResponse.bad_request("Цех не активен либо не найден")

    async def transform(
        self,
        dto: WorkshopScheduleByDayDTO,
        active_workshop_schedule: WorkshopScheduleModel,
    ) -> List[WorkshopScheduleSpaceDTO]:
        return await self._generate_schedule(
            schedule_date=dto.schedule_date, active_schedule=active_workshop_schedule
        )

    async def _generate_schedule(
        self, schedule_date: date, active_schedule: WorkshopScheduleModel
    ) -> List[WorkshopScheduleSpaceDTO]:
        time_start = time(0, 0, 59)
        time_end = time(23, 59, 59)
        date_start = datetime.combine(schedule_date, time_start)
        date_end = datetime.combine(schedule_date, time_end)

        # Получение расписаний с фильтрацией
        schedules = await self.schedule_repository.get_with_filters(
            filters=[
                and_(
                    self.schedule_repository.model.is_active.is_(True),
                    self.schedule_repository.model.start_at >= date_start,
                    self.schedule_repository.model.start_at <= date_end,
                )
            ]
        )

        planned_schedules = []
        current_time_dt = datetime.combine(datetime.today(), datetime.now().time())

        # Корректировка времени для указанной даты
        if schedule_date > current_time_dt.date():
            current_time_dt = datetime.combine(schedule_date, active_schedule.start_at)
        elif schedule_date == current_time_dt.date():
            current_time_dt = self._adjust_current_time(
                current_time_dt, active_schedule
            )
        else:
            raise AppExceptionResponse.bad_request(
                "Нельзя получить расписание для прошедших дат."
            )

        # Генерация расписания
        planned_schedules = self._create_schedule_intervals(
            current_time_dt, schedule_date, active_schedule, schedules
        )

        return planned_schedules

    def _adjust_current_time(self, current_time_dt, active_schedule):
        """
        Корректирует текущее время для расписания на сегодня.
        """
        start_time_dt = datetime.combine(datetime.today(), active_schedule.start_at)

        if current_time_dt.time() > active_schedule.start_at:
            time_diff = (current_time_dt - start_time_dt).total_seconds()
            interval_minutes = (
                active_schedule.car_service_min
                + active_schedule.break_between_service_min
            )
            full_intervals_passed = time_diff // (interval_minutes * 60)
            adjusted_start_time = start_time_dt + timedelta(
                minutes=(full_intervals_passed + 1) * interval_minutes
            )
            return max(adjusted_start_time, current_time_dt)
        return start_time_dt

    def _create_schedule_intervals(
        self, current_time_dt, schedule_date, active_schedule, schedules
    ):
        """
        Генерация расписания на основе интервалов работы.
        """
        planned_schedules = []
        interval_minutes = (
            active_schedule.car_service_min + active_schedule.break_between_service_min
        )

        while current_time_dt.time() < active_schedule.end_at:
            service_end_time = current_time_dt + timedelta(
                minutes=active_schedule.car_service_min
            )

            if service_end_time.time() > active_schedule.end_at:
                break

            # Фильтрация записей для текущего интервала
            filtered_items = [
                item
                for item in schedules
                if item.start_at
                == datetime.combine(schedule_date, current_time_dt.time())
            ]
            free_space = max(
                0, active_schedule.machine_at_one_time - len(filtered_items)
            )

            if free_space > 0:
                planned_schedules.append(
                    WorkshopScheduleSpaceDTO(
                        workshop_schedule_id=active_schedule.id,
                        scheduled_data=schedule_date,
                        start_at=current_time_dt.time(),
                        end_at=service_end_time.time(),
                        free_space=free_space,
                    )
                )
            current_time_dt = service_end_time + timedelta(
                minutes=active_schedule.break_between_service_min
            )

        return planned_schedules
