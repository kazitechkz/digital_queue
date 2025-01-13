from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.schedule.create_schedule_dto import CreateScheduleDTO
from app.adapters.dto.schedule.schedule_dto import ScheduleWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.schedule.client.create_client_schedule_case import CreateClientScheduleCase


class ScheduleApi:

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()


    def _add_routes(self) -> None:
        self.router.post(
            f"{AppPathConstants.CreateClientSchedulePathName}",
            response_model=ScheduleWithRelationsDTO,
            summary="Создать расписание",
            description="Создание расписания для юр.лица и физ.лица",
        )(self.create_schedule)

    async def create_schedule(
            self,
            dto:CreateScheduleDTO,
            user:UserWithRelationsDTO = Depends(check_client),
            db: AsyncSession = Depends(get_db)
    ):
        use_case = CreateClientScheduleCase(db)
        try:
            return await use_case.execute(dto=dto,user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении материала",
                extra={"details": str(exc)},
                is_custom=True,
            )
