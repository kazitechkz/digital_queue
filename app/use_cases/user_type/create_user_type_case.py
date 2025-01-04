from typing import List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_type.user_type_dto import UserTypeCDTO, UserTypeRDTO
from app.adapters.repositories.user_type.user_type_repository import \
    UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateUserTypeCase(BaseUseCase[UserTypeRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserTypeRepository(db)

    async def execute(self, dto: UserTypeCDTO) -> UserTypeRDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        return UserTypeRDTO.from_orm(data)

    async def validate(self, dto: UserTypeCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == dto.value.lower()]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Тип пользователя с таким значением уже существует"
            )
        return self.repository.model(**dto.dict())
