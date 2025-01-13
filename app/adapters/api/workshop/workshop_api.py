from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop.workshop_dto import (
    WorkshopCDTO,
    WorkshopWithRelationsDTO,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.path_constants import AppPathConstants
from app.use_cases.file.save_file_case import SaveFileCase
from app.use_cases.workshop.all_workshop_case import AllWorkshopCase
from app.use_cases.workshop.create_workshop_case import CreateWorkshopCase
from app.use_cases.workshop.delete_workshop_case import DeleteWorkshopCase
from app.use_cases.workshop.get_workshop_by_id_case import GetWorkshopByIdCase
from app.use_cases.workshop.get_workshop_by_value_case import GetWorkshopByValueCase
from app.use_cases.workshop.update_workshop_case import UpdateWorkshopCase


class WorkshopApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=list[WorkshopWithRelationsDTO],
            summary="Список цехов",
            description="Получение списка цехов",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=WorkshopWithRelationsDTO,
            summary="Создать цех в системе",
            description="Создание цехов в системе",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=WorkshopWithRelationsDTO,
            summary="Обновить цех по уникальному ID",
            description="Обновление цеха по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите цех по уникальному ID",
            description="Удаление цеха по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=WorkshopWithRelationsDTO,
            summary="Получить цех по уникальному ID",
            description="Получение цеха по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=WorkshopWithRelationsDTO,
            summary="Получить цех по уникальному значению SAP",
            description="Получение цеха по уникальному значению в системе SAP",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllWorkshopCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении цеха",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetWorkshopByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении цеха по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: WorkshopCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        file_case = SaveFileCase(db)
        use_case = CreateWorkshopCase(db)
        file_model = None
        try:
            if AppFileExtensionConstants.is_upload_file(file):
                file_model = await file_case.execute(
                    file=file,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                    uploaded_folder=AppFileExtensionConstants.WorkshopFolderName,
                )
            return await use_case.execute(dto=dto, file=file_model)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании цеха",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: WorkshopCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateWorkshopCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении бизнес процесса",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteWorkshopCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении цеха",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, sap_id: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetWorkshopByValueCase(db)
        try:
            return await use_case.execute(value=sap_id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении цеха по значению SAP ID",
                extra={"value": sap_id, "details": str(exc)},
                is_custom=True,
            )
