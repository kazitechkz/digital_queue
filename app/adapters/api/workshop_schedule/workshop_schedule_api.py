from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_by_day_dto import WorkshopScheduleByDayDTO
from app.adapters.dto.workshop_schedule.workshop_schedule_dto import (
    WorkshopScheduleCDTO,
    WorkshopScheduleWithRelationsDTO,
)
from app.adapters.dto.workshop_schedule.workshop_schedule_space_dto import WorkshopScheduleSpaceDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.workshop_schedule.all_workshop_schedule_case import (
    AllWorkshopScheduleCase,
)
from app.use_cases.workshop_schedule.create_workshop_schedule_case import (
    CreateWorkshopScheduleCase,
)
from app.use_cases.workshop_schedule.delete_workshop_schedule_case import (
    DeleteWorkshopScheduleCase,
)
from app.use_cases.workshop_schedule.get_workshop_schedule_by_day_case import GetWorkshopScheduleByDayCase
from app.use_cases.workshop_schedule.get_workshop_schedule_by_id_case import (
    GetWorkshopScheduleByIdCase,
)
from app.use_cases.workshop_schedule.get_workshop_schedule_by_value_case import (
    GetWorkshopScheduleByValueCase,
)
from app.use_cases.workshop_schedule.update_workshop_schedule_case import (
    UpdateWorkshopScheduleCase,
)


class WorkshopScheduleApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=list[WorkshopScheduleWithRelationsDTO],
            summary="Список расписаний цеха",
            description="Получение списка расписаний цеха",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=WorkshopScheduleWithRelationsDTO,
            summary="Создать расписание цеха",
            description="Создание расписаний цеха",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=WorkshopScheduleWithRelationsDTO,
            summary="Обновить расписание цеха по уникальному ID",
            description="Обновление расписаний цеха по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите расписание цеха по уникальному ID",
            description="Удаление расписаний цеха по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=WorkshopScheduleWithRelationsDTO,
            summary="Получить расписание цеха по уникальному ID",
            description="Получение расписаний цеха по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=WorkshopScheduleWithRelationsDTO,
            summary="Получить расписание цеха по уникальному значению",
            description="Получение расписаний цеха по уникальному значению",
        )(self.get_by_value)
        self.router.get(
            f"{AppPathConstants.GetFreeSpacePathName}",
            response_model=list[WorkshopScheduleSpaceDTO],
            summary="Получить расписание цеха",
            description="Получение расписаний цеха",
        )(self.get_free_space_path)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllWorkshopScheduleCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех расписаний цеха",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetWorkshopScheduleByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении расписаний цеха по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self, dto: WorkshopScheduleCDTO, db: AsyncSession = Depends(get_db)
    ):
        use_case = CreateWorkshopScheduleCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании расписания цеха",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: WorkshopScheduleCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateWorkshopScheduleCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании расписаний цеха",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteWorkshopScheduleCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании расписания цеха",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetWorkshopScheduleByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении расписания цеха по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )

    async def get_free_space_path(
            self, dto:WorkshopScheduleByDayDTO = Depends(), db: AsyncSession = Depends(get_db)
    ):
        use_case = GetWorkshopScheduleByDayCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении расписания цеха",
                extra={"details": str(exc)},
                is_custom=True,
            )