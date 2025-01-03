from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.pagination_dto import PaginationFileRDTO
from app.adapters.filters.file.file_filter import FileFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.file.delete_file_case import DeleteFileCase
from app.use_cases.file.get_file_by_id_case import GetFileByIdCase
from app.use_cases.file.paginate_file_case import PaginateFileCase
from app.use_cases.file.save_file_case import SaveFileCase
from app.use_cases.file.update_file_case import UpdateFileCase


class FileApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=PaginationFileRDTO,
            summary="Список файлов",
            description="Получение списка файлов",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=FileRDTO,
            summary="Создать файл в системе",
            description="Создание файлов в системе",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=FileRDTO,
            summary="Обновить файл по уникальному ID",
            description="Обновление файла по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите файл по уникальному ID",
            description="Удаление файла по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=FileRDTO,
            summary="Получить файл по уникальному ID",
            description="Получение файла по уникальному идентификатору",
        )(self.get)

    async def get_all(self,parameters:FileFilter=Depends(), db: AsyncSession = Depends(get_db)):
        use_case = PaginateFileCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении файла",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetFileByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении файла по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        folder_name:str = Query(description="Наименование папки"),
        file: UploadFile = File(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = SaveFileCase(db)
        try:
            return await use_case.execute(file=file,uploaded_folder=folder_name)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании файла",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        file: UploadFile = File(),
        folder_name: str = Query(description="Наименование папки"),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateFileCase(db)
        try:
            return await use_case.execute(id=id, uploaded_folder=folder_name, file=file)
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
        use_case = DeleteFileCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении файла",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )
