from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_user.verified_user_dto import (
    VerifiedUserCDTO, VerifiedUserWithRelationsDTO)
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.verified_user.verified_user_repository import \
    VerifiedUserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateVerifiedUserCase(BaseUseCase[VerifiedUserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedUserRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(self, dto: VerifiedUserCDTO) -> VerifiedUserWithRelationsDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        if not data:
            raise AppExceptionResponse.internal_error(
                "Проверенный пользователь не создан"
            )
        existed = await self.repository.get(
            id=data.id,
            options=self.repository.default_relationships(),
        )
        return VerifiedUserWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: VerifiedUserCDTO):
        existed_user = await self.user_repository.get(id=dto.user_id)
        if not existed_user:
            raise AppExceptionResponse.bad_request("Пользователь не найден")
        dto.iin = existed_user.iin
        dto.sid = existed_user.sid
        return self.repository.model(**dto.dict())
