from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_type.user_type_dto import UserTypeRDTO
from app.adapters.repositories.user_type.user_type_repository import \
    UserTypeRepository
from app.use_cases.base_case import BaseUseCase


class AllUserTypeCase(BaseUseCase[list[UserTypeRDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = UserTypeRepository(db)

    async def execute(self) -> list[UserTypeRDTO]:
        models = await self.repository.get_all()
        return [UserTypeRDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
