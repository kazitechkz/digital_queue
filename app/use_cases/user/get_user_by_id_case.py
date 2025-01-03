from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetUserByIdCase(BaseUseCase[UserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def execute(self, id: int) -> UserWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Пользователь не найден")
        return UserWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
