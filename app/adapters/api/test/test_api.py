from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleCDTO
from app.adapters.dto.workshop_schedule.workshop_schedule_by_day_dto import (
    WorkshopScheduleByDayDTO,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.api_clients.sap.sap_get_contract_client import (
    SapGetContractApiClient,
)
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.dto_constants import DTOConstant
from app.use_cases.file.save_file_case import SaveFileCase
from app.use_cases.workshop_schedule.get_workshop_schedule_by_day_case import (
    GetWorkshopScheduleByDayCase,
)


class TestApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            "/test-post",
            summary="Тестовый сервис",
            description="Тест",
        )(self.post_test)

        self.router.get(
            "/test-get",
            summary="Тестовый сервис",
            description="Тест",
        )(self.get_test)

    async def post_test(
        self,
        dto: RoleCDTO = Form(),
        file: UploadFile = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = SaveFileCase(db)
        try:
            print(type(file))
            return AppFileExtensionConstants.is_upload_file(file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании бизнес процесса",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get_test(
        self,
        dto: WorkshopScheduleByDayDTO = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        try:
            service = SapGetContractApiClient()
            use_case = GetWorkshopScheduleByDayCase(db)
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании бизнес процесса",
                extra={"details": str(exc)},
                is_custom=True,
            )
