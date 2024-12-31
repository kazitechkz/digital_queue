from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.file.file_repository import FileRepository
from app.infrastructure.services.file_service import FileService
from app.use_cases.base_case import BaseUseCase


class DeleteFileCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.repository = FileRepository(db)
        self.service = FileService(db)

    async def execute(self, id: int) -> bool:
        is_deleted = await self.service.delete_file(file_id=id)
        if is_deleted:
            return await self.repository.delete(id=id)
        return False

    async def validate(self):
        pass
