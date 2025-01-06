from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.auth.login_dto import LoginDTO
from app.adapters.dto.auth.token_dto import BearerTokenDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user
from app.infrastructure.database import get_db
from app.use_cases.auth.login_case import LoginCase


class AuthApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            "/login",
            response_model=BearerTokenDTO,
            summary="Авторизация",
            description="Авторизуйтесь с помощью username и password",
        )(self.sign_in)
        self.router.get(
            "/me",
            response_model=UserWithRelationsDTO,
            summary="Получить авторизованного пользователя",
            description="Данные пользователя",
        )(self.me)

    async def sign_in(self, dto: LoginDTO, db: AsyncSession = Depends(get_db)):
        use_case = LoginCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при логинации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def me(self, user: UserWithRelationsDTO = Depends(get_current_user)):
        try:
            return user
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при логинации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )
