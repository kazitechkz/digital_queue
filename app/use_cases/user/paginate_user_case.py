from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationUserWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.user.user_filter import UserFilter
from app.adapters.repositories.user.user_repository import UserRepository
from app.use_cases.base_case import BaseUseCase


class PaginateUserCase(BaseUseCase[PaginationUserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def execute(self, filter: UserFilter) -> PaginationUserWithRelationsDTO:
        models = await self.repository.paginate(
            dto=UserWithRelationsDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
        )
        return models

    async def validate(self):
        pass
