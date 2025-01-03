from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.repositories.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetFileByIdCase(BaseUseCase[FileRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = FileRepository(db)

    async def execute(self, id: int) -> FileRDTO:
        model = await self.repository.get(
            id,
        )
        if not model:
            raise AppExceptionResponse.not_found("Файл не найден")
        return FileRDTO.from_orm(model)

    async def validate(self):
        pass
