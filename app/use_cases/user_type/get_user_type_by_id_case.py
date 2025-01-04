from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_type.user_type_dto import UserTypeRDTO
from app.adapters.repositories.user_type.user_type_repository import \
    UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetUserTypeByIdCase(BaseUseCase[UserTypeRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserTypeRepository(db)

    async def execute(self, id: int) -> UserTypeRDTO:
        model = await self.repository.get(id)
        if not model:
            raise AppExceptionResponse.not_found("Тип пользователя не найден")
        return UserTypeRDTO.from_orm(model)

    async def validate(self):
        pass
