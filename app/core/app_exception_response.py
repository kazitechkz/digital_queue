import logging

from fastapi import HTTPException, status

from app.infrastructure.config import app_config


class AppExceptionResponse:
    """Утилита для создания стандартных HTTP-исключений."""

    logger = logging.getLogger("AppExceptionResponse")

    @staticmethod
    def create_exception(
        status_code: int,
        message: str,
        extra: dict | None = None,
        is_custom: bool = True,
    ) -> HTTPException:
        """
        Создаёт HTTP-исключение с возможностью добавления дополнительных данных.

        Args:
            status_code (int): Код статуса HTTP.
            message (str): Сообщение об ошибке.
            extra (dict, optional): Дополнительные данные, которые будут включены в `detail`.

        Returns:
            HTTPException: Объект HTTP-исключения.
        """
        detail = {"message": message, "is_custom": is_custom}
        if extra:
            detail.update(extra)

        # Логгирование ошибки
        AppExceptionResponse.logger.error(f"Error {status_code}: {detail}")

        return HTTPException(status_code=status_code, detail=detail)

    @staticmethod
    def bad_request(message: str = "Плохой запрос", extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_400_BAD_REQUEST, message=message, extra=extra
        )

    @staticmethod
    def unauthorized(message: str = "Не авторизован", extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_401_UNAUTHORIZED, message=message, extra=extra
        )

    @staticmethod
    def forbidden(message: str = "Доступ запрещен", extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_403_FORBIDDEN, message=message, extra=extra
        )

    @staticmethod
    def not_found(message: str = "Ресурс не найден", extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_404_NOT_FOUND, message=message, extra=extra
        )

    @staticmethod
    def conflict(message: str = "Conflict occurred", extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_409_CONFLICT, message=message, extra=extra
        )

    @staticmethod
    def internal_error(
        message: str = "Ошибка сервера",
        extra: dict | None = None,
        is_custom: bool = False,  # Указывает, что это не кастомная ошибка
    ):
        if app_config.app_status.lower() == "production":
            extra["details"] = "Ошибка сервиса"
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            extra=extra,
            is_custom=is_custom,
        )
