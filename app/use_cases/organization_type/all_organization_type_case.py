from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_type.organization_type_dto import (
    OrganizationTypeRDTO,
)
from app.adapters.repositories.organization_type.organization_type_repository import (
    OrganizationTypeRepository,
)
from app.use_cases.base_case import BaseUseCase


class AllOrganizationTypeCase(BaseUseCase[list[OrganizationTypeRDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationTypeRepository(db)

    async def execute(self) -> list[OrganizationTypeRDTO]:
        models = await self.repository.get_all()
        return [OrganizationTypeRDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
