from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_type.user_type_dto import UserTypeCDTO, UserTypeRDTO
from app.adapters.repositories.user_type.user_type_repository import UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class UpdateUserTypeCase(BaseUseCase[UserTypeRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserTypeRepository(db)

    async def execute(self, id: int, dto: UserTypeCDTO) -> UserTypeRDTO:
        obj = await self.validate(id=id, dto=dto)
        data = await self.repository.update(obj=obj, dto=dto)
        return UserTypeRDTO.from_orm(data)

    async def validate(self, id: int, dto: UserTypeCDTO):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Тип пользователя не найдена")
        if await self.repository.get_first_with_filters(
            [
                func.lower(self.repository.model.value) == dto.value.lower(),
                self.repository.model.id != id,
            ]
        ):
            raise AppExceptionResponse.bad_request(
                "Тип пользователя с таким значением уже существует"
            )
        return existed
