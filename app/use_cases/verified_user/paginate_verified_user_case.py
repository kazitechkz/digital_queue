from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import \
    PaginationVerifiedUserWithRelationsDTO
from app.adapters.dto.verified_user.verified_user_dto import \
    VerifiedUserWithRelationsDTO
from app.adapters.filters.verified_user.verified_user_filter import \
    VerifiedUserFilter
from app.adapters.repositories.verified_user.verified_user_repository import \
    VerifiedUserRepository
from app.use_cases.base_case import BaseUseCase


class PaginateVerifiedUserCase(BaseUseCase[PaginationVerifiedUserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedUserRepository(db)

    async def execute(
        self, filter: VerifiedUserFilter
    ) -> PaginationVerifiedUserWithRelationsDTO:
        models = await self.repository.paginate(
            dto=VerifiedUserWithRelationsDTO,
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
