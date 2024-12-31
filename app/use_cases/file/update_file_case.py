from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.repositories.file.file_repository import FileRepository
from app.infrastructure.services.file_service import FileService
from app.use_cases.base_case import BaseUseCase


class UpdateFileCase(BaseUseCase[FileRDTO]):
    def __init__(self, db: AsyncSession):
        self.service = FileService(db)

    async def execute(
        self, file: UploadFile, uploaded_folder: str, id: int, extensions=None
    ) -> FileRDTO:
        file = await self.service.update_file(
            file_id=id,
            new_file=file,
            uploaded_folder=uploaded_folder,
            extensions=extensions,
        )
        return FileRDTO.from_orm(file)

    async def validate(self):
        pass
