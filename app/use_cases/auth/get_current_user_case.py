from datetime import datetime, timedelta

from jose import jwt
from keycloak import KeycloakAuthenticationError
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import (UserKeycloakCDTO,
                                            UserWithRelationsDTO)
from app.adapters.dto.user.user_response_dto import UserResponseDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.user_type.user_type_repository import \
    UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.key_cloak_core import keycloak_openid
from app.infrastructure.api_clients.user_repo.user_repo_client import UserRepoApiClient
from app.infrastructure.config import app_config
from app.use_cases.base_case import BaseUseCase


class GetCurrentUserCase(BaseUseCase[UserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
        self.user_type_repository = UserTypeRepository(db)

    async def execute(self, token: str) -> UserWithRelationsDTO:
        if app_config.is_keycloak_auth():
            try:
                user_info: dict = keycloak_openid.userinfo(token)
                dto = UserKeycloakCDTO.parse_obj(user_info)
                dto.sid = user_info["sub"]
                dto = await self.transform(dto=dto, token=token)
                existed = await self.repository.get_first_with_filters(
                    filters=[
                        and_(func.lower(self.repository.model.sid) == dto.sid.lower())
                    ],
                    options=self.repository.default_relationships(),
                )
                if existed:
                    check_time = existed.updated_at + timedelta(
                        minutes=app_config.update_user_info_minutes
                    )
                    if check_time < datetime.now():
                        existed = await self.repository.update(obj=existed, dto=dto)
                        existed = await self.repository.get_first_with_filters(
                            filters=[
                                and_(
                                    func.lower(self.repository.model.sid)
                                    == dto.sid.lower()
                                )
                            ],
                            options=self.repository.default_relationships(),
                        )
                    return UserWithRelationsDTO.from_orm(existed)
                else:
                    user_repo_client = UserRepoApiClient(token=token)
                    if app_config.allow_fake_user_info:
                        fake_dict: dict = user_repo_client.generate_fake_mobile_iin()
                        dto.iin = fake_dict["iin"]
                        dto.phone = fake_dict["mobile"]
                    else:
                        userRepoDTO: UserResponseDTO = (
                            await user_repo_client.get_current_user()
                        )
                        dto.iin = userRepoDTO.additional_attributes.iin
                        dto.phone = userRepoDTO.mobile
                    model = await self.repository.create(
                        obj=self.repository.model(**dto.dict())
                    )
                    model = await self.repository.get(
                        id=model.id, options=self.repository.default_relationships()
                    )
                    return UserWithRelationsDTO.from_orm(model)

            except KeycloakAuthenticationError as e:
                raise AppExceptionResponse.internal_error(
                    message=f"Произошла ошибка {str(e.error_message)}",
                )
        else:
            user_data: dict = self.local_verify_jwt_token(token)
            expire = user_data.get("exp")
            if not expire or int(expire) < datetime.now().timestamp():
                raise AppExceptionResponse.unauthorized(message="Токен не действителен")
            user_id = int(user_data.get("sub"))
            if not user_id:
                raise AppExceptionResponse.unauthorized(
                    message="Пользователь не найден"
                )
            user = await self.repository.get(
                id=user_id, options=self.repository.default_relationships()
            )
            return UserWithRelationsDTO.from_orm(user)

    async def validate(self):
        pass

    async def transform(self, dto: UserKeycloakCDTO, token: str) -> UserKeycloakCDTO:
        roles = await self.get_roles(token=token)
        existed = await self.role_repository.get_first_with_filters(
            filters=[func.lower(self.role_repository.model.keycloak_value) in roles]
        )
        if "digital_queue_client_legal" in roles:
            dto.type_id = 2
        else:
            dto.type_id = 1
        if existed:
            dto.role_id = existed.id
        else:
            dto.role_id = 7
        return dto

    async def get_roles(self, token: str):
        try:
            decoded_token = keycloak_openid.decode_token(
                token,
            )
            roles = decoded_token.get("realm_access", {}).get("roles", [])
            return [role.lower() for role in roles]
        except Exception as e:
            raise AppExceptionResponse.internal_error(message=f"Токен не распознан {e}")

    def local_verify_jwt_token(self, token: str) -> dict:
        try:
            decoded_data = jwt.decode(
                token, app_config.secret_key, algorithms=app_config.algorithm
            )
            # Проверяем, что это именно Access Token, а не Refresh Token
            if decoded_data.get("type") != "access":
                raise AppExceptionResponse.forbidden(
                    message="Недопустимый токен для доступа к ресурсу",
                )
            return decoded_data
        except jwt.JWTError as jwtError:
            raise AppExceptionResponse.unauthorized(
                message=f"Не удалось проверить токен {jwtError!s}",
            )
