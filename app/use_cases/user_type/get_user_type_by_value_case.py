from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_type.user_type_dto import UserTypeRDTO
from app.adapters.repositories.user_type.user_type_repository import UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetUserTypeByValueCase(BaseUseCase[UserTypeRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserTypeRepository(db)

    async def execute(self, value: str) -> UserTypeRDTO:
        filters = [
            or_(
                func.lower(self.repository.model.value) == value.lower(),
                func.lower(self.repository.model.keycloak_value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(filters=filters)
        if not model:
            raise AppExceptionResponse.not_found("Тип пользователя не найден")
        return UserTypeRDTO.from_orm(model)

    async def validate(self):
        pass
