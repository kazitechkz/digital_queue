from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.user_type.user_type_repository import UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class DeleteUserTypeCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.repository = UserTypeRepository(db)

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Тип пользователя не найден")
        if existed.value in AppDbValueConstants.IMMUTABLE_USER_TYPES:
            raise AppExceptionResponse.bad_request(
                message="Тип пользователя нельзя удалять"
            )
