from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.pagination_dto import PaginationFileRDTO
from app.adapters.filters.file.file_filter import FileFilter
from app.adapters.repositories.file.file_repository import FileRepository
from app.use_cases.base_case import BaseUseCase


class PaginateFileCase(BaseUseCase[list[FileRDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = FileRepository(db)

    async def execute(self, filter: FileFilter) -> list[PaginationFileRDTO]:
        models = await self.repository.paginate(
            dto=FileRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
        )
        return models

    async def validate(self):
        pass
