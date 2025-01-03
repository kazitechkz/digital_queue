from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetUserByValueCase(BaseUseCase[UserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def execute(self, value: str) -> UserWithRelationsDTO:
        filters = [
            or_(
                func.lower(self.repository.model.sid) == value.lower(),
                func.lower(self.repository.model.preferred_username) == value.lower(),
                func.lower(self.repository.model.iin) == value.lower(),
                func.lower(self.repository.model.email) == value.lower(),
                func.lower(self.repository.model.phone) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Пользователь не найден")
        return UserWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
