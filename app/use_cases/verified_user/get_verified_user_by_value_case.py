from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_user.verified_user_dto import (
    VerifiedUserWithRelationsDTO,
)
from app.adapters.repositories.verified_user.verified_user_repository import (
    VerifiedUserRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVerifiedUserByValueCase(BaseUseCase[VerifiedUserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedUserRepository(db)

    async def execute(self, value: str) -> VerifiedUserWithRelationsDTO:
        filters = [
            or_(
                func.lower(self.repository.model.iin) == value.lower(),
                func.lower(self.repository.model.sid) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters, options=self.repository.default_relationships()
        )
        if not model:
            raise AppExceptionResponse.not_found(
                "Верифицированный пользователь не найден"
            )
        return VerifiedUserWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
