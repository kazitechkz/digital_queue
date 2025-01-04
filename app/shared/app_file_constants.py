from typing import Any

from starlette.datastructures import UploadFile


class AppFileExtensionConstants:
    FactoryFolderName = "factories"
    WorkshopFolderName = "workshops"
    MaterialFolderName = "materials"
    UserFolderName = "users"
    OrganizationFolderName = "organizations"
    VehicleFolderName = "vehicles"
    # Расширения для изображений
    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
        ".tiff",
        ".ico",
        ".heic",
    }

    # Расширения для видео
    VIDEO_EXTENSIONS = {
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".flv",
        ".wmv",
        ".webm",
        ".mpeg",
        ".3gp",
        ".m4v",
    }

    # Расширения для аудио
    AUDIO_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".ogg",
        ".m4a",
        ".wma",
        ".amr",
        ".opus",
        ".aiff",
    }

    # Расширения для документов
    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".csv",
        ".rtf",
        ".odt",
        ".ods",
        ".odp",
        ".epub",
        ".pages",
        ".numbers",
        ".key",
    }

    # Расширения для архивов
    ARCHIVE_EXTENSIONS = {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".iso",
        ".tgz",
        ".tar.gz",
    }

    # Расширения для текстовых файлов
    TEXT_EXTENSIONS = {
        ".txt",
        ".log",
        ".md",
        ".yaml",
        ".yml",
        ".json",
        ".xml",
        ".html",
        ".css",
        ".js",
    }

    # Все расширения
    ALL_EXTENSIONS = (
        IMAGE_EXTENSIONS
        | VIDEO_EXTENSIONS
        | AUDIO_EXTENSIONS
        | DOCUMENT_EXTENSIONS
        | ARCHIVE_EXTENSIONS
        | TEXT_EXTENSIONS
    )

    @staticmethod
    def is_valid_extension(extension: str, allowed_extensions: set) -> bool:
        """
        Проверяет, является ли расширение файла допустимым.

        Args:
            extension (str): Расширение файла (например, '.jpg').
            allowed_extensions (set): Набор допустимых расширений.

        Returns:
            bool: True, если расширение допустимо, иначе False.
        """
        return extension.lower() in allowed_extensions

    @staticmethod
    def is_upload_file(obj: Any) -> bool:
        return isinstance(obj, UploadFile)
