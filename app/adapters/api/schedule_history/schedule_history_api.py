from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.schedule_history.employee.take_schedule_case import TakeScheduleCase


class ScheduleApi:

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()


    def _add_routes(self) -> None:
        self.router.post(
            f"{AppPathConstants.TakeScheduleHistoryByIdPathName}",
            response_model=ScheduleHistoryWithRelationsDTO,
            summary="Взять расписание",
            description="Взятие расписания",
        )(self.take_schedule_history)

    async def take_schedule_history(
            self,
            id:AppPathConstants.IDPath,
            user:UserWithRelationsDTO = Depends(check_client),
            db: AsyncSession = Depends(get_db)
    ):
        use_case = TakeScheduleCase(db)
        try:
            return await use_case.execute(schedule_id=id,user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении материала",
                extra={"details": str(exc)},
                is_custom=True,
            )