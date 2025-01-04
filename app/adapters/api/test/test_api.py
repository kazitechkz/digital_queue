import json
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.pagination_dto import (Pagination,
                                             PaginationUserWithRelationsDTO)
from app.adapters.dto.role.role_dto import RoleCDTO
from app.adapters.dto.user.user_dto import UserRDTO, UserWithRelationsDTO
from app.adapters.filters.user.user_filter import UserFilter
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.query_constants import AppQueryConstants
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

        self.router.get(
            "/test-get",
            summary="Тестовый сервис",
            description="Тест",
            response_model=PaginationUserWithRelationsDTO,
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
        params: UserFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        try:
            userRepo = UserRepository(db=db)
            all = await userRepo.paginate(
                per_page=params.per_page,
                page=params.page,
                filters=params.apply(),
                dto=UserWithRelationsDTO,
                order_by=params.order_by,
                order_direction=params.order_direction,
                options=userRepo.default_relationships(),
            )
            return all
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании бизнес процесса",
                extra={"details": str(exc)},
                is_custom=True,
            )
