from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.material.material_dto import MaterialWithRelationsDTO, MaterialCDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.path_constants import AppPathConstants
from app.use_cases.file.save_file_case import SaveFileCase
from app.use_cases.material.all_material_case import AllMaterialCase
from app.use_cases.material.create_material_case import CreateMaterialCase
from app.use_cases.material.delete_material_case import DeleteMaterialCase
from app.use_cases.material.get_material_by_id_case import GetMaterialByIdCase
from app.use_cases.material.get_material_by_value_case import GetMaterialByValueCase
from app.use_cases.material.update_material_case import UpdateMaterialCase


class MaterialApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[MaterialWithRelationsDTO],
            summary="Список материалов",
            description="Получение списка материалов",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=MaterialWithRelationsDTO,
            summary="Создать материал в системе",
            description="Создание материалов в системе",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=MaterialWithRelationsDTO,
            summary="Обновить материал по уникальному ID",
            description="Обновление материала по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите материал по уникальному ID",
            description="Удаление материала по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=MaterialWithRelationsDTO,
            summary="Получить материал по уникальному ID",
            description="Получение материала по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-sap-id/{sap_id}",
            response_model=MaterialWithRelationsDTO,
            summary="Получить материал по уникальному значению SAP",
            description="Получение материала по уникальному значению в системе SAP",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllMaterialCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении материала",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetMaterialByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении материала по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: MaterialCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        file_case = SaveFileCase(db)
        use_case = CreateMaterialCase(db)
        file_model = None
        try:
            if file is not None:
                file_model = await file_case.execute(
                    file=file,
                    extensions=AppFileExtensionConstants.IMAGE_EXTENSIONS,
                    uploaded_folder=AppFileExtensionConstants.MaterialFolderName,
                )
            return await use_case.execute(dto=dto, file=file_model)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании материала",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: MaterialCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateMaterialCase(db)
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
        use_case = DeleteMaterialCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении материала",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, sap_id: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetMaterialByValueCase(db)
        try:
            return await use_case.execute(value=sap_id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении материала по значению SAP ID",
                extra={"value": sap_id, "details": str(exc)},
                is_custom=True,
            )
