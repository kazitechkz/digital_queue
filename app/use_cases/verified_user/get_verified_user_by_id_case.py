from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_user.verified_user_dto import (
    VerifiedUserWithRelationsDTO,
)
from app.adapters.repositories.verified_user.verified_user_repository import (
    VerifiedUserRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVerifiedUserByIdCase(BaseUseCase[VerifiedUserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedUserRepository(db)

    async def execute(self, id: int) -> VerifiedUserWithRelationsDTO:
        model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        if not model:
            raise AppExceptionResponse.not_found(
                "Верифицированный пользователь не найден"
            )
        return VerifiedUserWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
