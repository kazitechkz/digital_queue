from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.factory.factory_dto import (FactoryCDTO,
                                                  FactoryWithRelationsDTO)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.path_constants import AppPathConstants
from app.use_cases.factory.all_factory_case import AllFactoryCase
from app.use_cases.factory.create_factory_case import CreateFactoryCase
from app.use_cases.factory.delete_factory_case import DeleteFactoryCase
from app.use_cases.factory.get_factory_by_id_case import GetFactoryByIdCase
from app.use_cases.factory.get_factory_by_value_case import \
    GetFactoryByValueCase
from app.use_cases.factory.update_factory_case import UpdateFactoryCase
from app.use_cases.file.save_file_case import SaveFileCase


class FactoryApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.create_factory_url = self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=list[FactoryWithRelationsDTO],
            summary="Список заводов",
            description="Получение списка заводов",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=FactoryWithRelationsDTO,
            summary="Создать завод в системе",
            description="Создание заводов в системе",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=FactoryWithRelationsDTO,
            summary="Обновитьзавод по уникальному ID",
            description="Обновление завода по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите завод по уникальному ID",
            description="Удаление завода по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=FactoryWithRelationsDTO,
            summary="Получить завод по уникальному ID",
            description="Получение завода по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=FactoryWithRelationsDTO,
            summary="Получить завод по уникальному значению SAP",
            description="Получение завода по уникальному значению в системе SAP",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllFactoryCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении завода",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetFactoryByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении завода по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: FactoryCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        file_case = SaveFileCase(db)
        use_case = CreateFactoryCase(db)
        file_model = None
        try:
            if AppFileExtensionConstants.is_upload_file(file):
                file_model = await file_case.execute(
                    file=file,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                    uploaded_folder=AppFileExtensionConstants.FactoryFolderName,
                )
            return await use_case.execute(dto=dto, file=file_model)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании завода",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: FactoryCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateFactoryCase(db)
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
        use_case = DeleteFactoryCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении завода",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetFactoryByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении завода по значению SAP ID",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
