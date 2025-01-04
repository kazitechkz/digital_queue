from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_user.verified_user_dto import (
    VerifiedUserCDTO,
    VerifiedUserWithRelationsDTO,
)
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.verified_user.verified_user_repository import (
    VerifiedUserRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import VerifiedUserModel
from app.use_cases.base_case import BaseUseCase


class UpdateVerifiedUserCase(BaseUseCase[VerifiedUserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedUserRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(
        self, id: int, dto: VerifiedUserCDTO
    ) -> VerifiedUserWithRelationsDTO:
        model = await self.validate(id=id, dto=dto)
        dto = await self.transform(model=model, dto=dto)
        data = await self.repository.update(obj=model, dto=dto)
        if not data:
            raise AppExceptionResponse.internal_error(
                "Проверенный пользователь не обновлен"
            )
        existed = await self.repository.get(
            id=data.id,
            options=self.repository.default_relationships(),
        )
        return VerifiedUserWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: VerifiedUserCDTO) -> VerifiedUserModel:
        model = await self.repository.get(id=id)
        if not model:
            raise AppExceptionResponse.not_found(
                message="Проверенный пользователь не найден"
            )
        existed_user = await self.user_repository.get(id=dto.user_id)
        if not existed_user:
            raise AppExceptionResponse.bad_request("Пользователь не найден")
        return model

    async def transform(
        self, model: VerifiedUserModel, dto: VerifiedUserCDTO
    ) -> VerifiedUserWithRelationsDTO:
        dto.sid = model.sid
        dto.iin = model.iin
        return dto
