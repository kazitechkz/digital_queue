from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleCDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_cases.file.save_file_case import SaveFileCase


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

    async def post_test(
        self,
        dto: RoleCDTO = Depends(),
        file: UploadFile = File(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = SaveFileCase(db)
        try:
            # file =  await use_case.execute(file=file, uploaded_folder="workshops",extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS)
            dto.keycloak_value = f"213123123123123"
            return dto
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании бизнес процесса",
                extra={"details": str(exc)},
                is_custom=True,
            )
