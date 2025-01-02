import os
import uuid
from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel
from app.infrastructure.config import app_config
from app.shared.app_file_constants import AppFileExtensionConstants


class FileService:
    UPLOAD_FOLDER = f"{app_config.static_folder}/{app_config.upload_folder}"
    ALLOWED_EXTENSIONS: dict = AppFileExtensionConstants.ALL_EXTENSIONS
    NOT_ALLOWED_EXTENSIONS = app_config.not_allowed_extensions
    MAX_FILE_SIZE_MB = app_config.app_upload_max_file_size_mb

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @staticmethod
    def generate_file_path(filename: str, directory: str) -> str:
        """
        Генерирует уникальный путь для файла.
        """
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        return os.path.join(directory, unique_name)

    @staticmethod
    def validate_file(file: UploadFile, extensions=None):
        """
        Проверяет размер файла и его расширение.
        """
        ALLOWED_EXTENSIONS = extensions or FileService.ALLOWED_EXTENSIONS

        # Проверка расширения
        _, extension = os.path.splitext(file.filename)
        if (
            extension.lower() not in ALLOWED_EXTENSIONS
            or extension.lower() in FileService.NOT_ALLOWED_EXTENSIONS
        ):
            raise AppExceptionResponse.bad_request(
                message=f"Недопустимое расширение файла. Допустимы: {list(ALLOWED_EXTENSIONS)}"
            )

        # Проверка размера
        file.file.seek(0, os.SEEK_END)
        file_size_mb = file.file.tell() / (1024 * 1024)
        file.file.seek(0)  # Возврат указателя файла в начало
        if file_size_mb > FileService.MAX_FILE_SIZE_MB:
            raise AppExceptionResponse.bad_request(
                message=f"Файл слишком большой. Максимальный размер: {FileService.MAX_FILE_SIZE_MB} МБ"
            )

    async def save_file(
        self, file: UploadFile, uploaded_folder: str, extensions: Optional[dict] = None
    ) -> FileModel:
        """
        Сохраняет файл в статичной папке и создает запись в базе данных.
        """
        try:
            # Проверка файла
            FileService.validate_file(file, extensions)

            # Создание папки, если не существует
            upload_directory = os.path.join(FileService.UPLOAD_FOLDER, uploaded_folder)
            os.makedirs(upload_directory, exist_ok=True)

            # Генерация пути
            file_path = FileService.generate_file_path(file.filename, upload_directory)

            # Сохранение файла
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Создание записи
            file_record = FileModel(
                filename=file.filename,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                content_type=file.content_type,
            )
            self.db.add(file_record)
            await self.db.commit()
            await self.db.refresh(file_record)
            return file_record
        except Exception as exc:
            await self.db.rollback()  # Откат транзакции в случае ошибки
            raise AppExceptionResponse.internal_error(
                message="Ошибка при сохранении файла",
                extra={"filename": file.filename, "details": str(exc)},
                is_custom=True,
            )

    async def delete_file(self, file_id: int, db: AsyncSession) -> bool:
        """
        Удаляет файл с диска и из базы данных.

        Args:
            file_id (int): ID файла.
            db (AsyncSession): Сессия базы данных.

        Returns:
            bool: Успех удаления.
        """
        try:
            # Поиск записи о файле в базе данных
            file_record = await db.get(FileModel, file_id)
            if not file_record:
                raise AppExceptionResponse.not_found(message="Файл не найден")

            # Удаление файла с диска
            if os.path.exists(file_record.file_path):
                os.remove(file_record.file_path)

            # Удаление записи из базы данных
            await db.delete(file_record)
            await db.commit()

            return True
        except Exception as exc:
            await db.rollback()  # Откат транзакции в случае ошибки
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении файла",
                extra={"file_id": file_id, "details": str(exc)},
                is_custom=True,
            )

    async def update_file(
        self,
        file_id: int,
        new_file: UploadFile,
        uploaded_folder: str,
        extensions: Optional[dict] = None,
    ) -> FileModel:
        """
        Обновляет файл на диске и запись в базе данных.

        Args:
            file_id (int): ID файла.
            new_file (UploadFile): Новый файл.
            db (AsyncSession): Сессия базы данных.

        Returns:
            FileModel: Обновленная запись.
        """
        try:
            existing_file = await self.db.get(FileModel, file_id)
            if not existing_file:
                raise AppExceptionResponse.not_found(message="Файл не найден")

            # Удаление старого файла
            if os.path.exists(existing_file.file_path):
                os.remove(existing_file.file_path)

            # Проверка файла
            FileService.validate_file(new_file, extensions)

            # Создание папки, если не существует
            upload_directory = os.path.join(FileService.UPLOAD_FOLDER, uploaded_folder)
            os.makedirs(upload_directory, exist_ok=True)

            # Генерация пути для нового файла
            new_file_path = FileService.generate_file_path(
                new_file.filename, upload_directory
            )

            # Сохранение нового файла
            with open(new_file_path, "wb") as f:
                f.write(await new_file.read())

            # Обновление записи в базе данных
            existing_file.filename = new_file.filename
            existing_file.file_path = new_file_path
            existing_file.file_size = os.path.getsize(new_file_path)
            existing_file.content_type = new_file.content_type
            await self.db.commit()
            await self.db.refresh(existing_file)
            return existing_file
        except Exception as exc:
            await self.db.rollback()
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении файла",
                extra={"file_id": file_id, "details": str(exc)},
                is_custom=True,
            )
