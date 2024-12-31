from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.repositories.file.file_repository import FileRepository
from app.infrastructure.services.file_service import FileService
from app.use_cases.base_case import BaseUseCase


class SaveFileCase(BaseUseCase[FileRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = FileRepository(db)
        self.service = FileService(db)

    async def execute(
        self, file: UploadFile, uploaded_folder: str, extensions=None
    ) -> FileRDTO:
        file = await self.service.save_file(
            file=file, uploaded_folder=uploaded_folder, extensions=extensions
        )
        file_existed = await self.repository.create(obj=file)
        return FileRDTO.from_orm(file_existed)

    async def validate(self):
        pass
