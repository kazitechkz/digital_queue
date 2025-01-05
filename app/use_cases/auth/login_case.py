from keycloak import KeycloakAuthenticationError
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.auth.login_dto import LoginDTO
from app.adapters.dto.auth.token_dto import BearerTokenDTO
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import verify_password, create_access_token, create_refresh_token
from app.core.key_cloak_core import keycloak_openid
from app.infrastructure.config import app_config
from app.use_cases.base_case import BaseUseCase


class LoginCase(BaseUseCase[BearerTokenDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def execute(self,dto:LoginDTO) -> BearerTokenDTO:
        if app_config.is_keycloak_auth():
            try:
                token = keycloak_openid.token(username=dto.username, password=dto.password)
                return BearerTokenDTO(
                    access_token=token["access_token"],
                    refresh_token=token["refresh_token"]
                )
            except KeycloakAuthenticationError:
                raise AppExceptionResponse.bad_request(
                    message="Неверные данные"
                )
        else:
            user = await self.repository.get_first_with_filters(filters=[
                and_(func.lower(self.repository.model.preferred_username) == dto.username)
            ])
            if not user:
                raise AppExceptionResponse.bad_request(
                    message="Неверные данные"
                )
            result = verify_password(dto.password, user.password_hash)
            if not result:
                raise AppExceptionResponse.bad_request(
                    message="Неверные данные"
                )
            access_token = create_access_token(data=user.id)
            refresh_token = create_refresh_token(data=user.id)
            return BearerTokenDTO(
                access_token=access_token,
                refresh_token=refresh_token
            )

    async def validate(self):
        pass