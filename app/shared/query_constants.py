from datetime import datetime
from typing import Annotated, Optional

from fastapi import Query

from app.infrastructure.config import app_config
from app.shared.field_constants import FieldConstants
from app.shared.validation_constants import app_validation


class AppQueryConstants:
    @staticmethod
    def StandardPerPageQuery(description="Количество элементов на странице"):
        return Query(
            gt=0,
            le=100,
            default=20,
            description=description,
        )

    @staticmethod
    def StandardPageQuery(description="Номер страницы"):
        return Query(
            gt=0,
            default=1,
            description=description,
        )

    @staticmethod
    def StandardOptionalSearchQuery(description="Поисковый запрос"):
        return Query(
            default=None,
            max_length=FieldConstants.STANDARD_LENGTH,
            min_length=2,
            description=description,
        )

    @staticmethod
    def StandardSortFieldQuery(description="Поле для сортировки"):
        return Query(
            default=None,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardSortFieldQuery(description="Сортировать по полю"):
        return Query(
            default="id",
            description=description,
        )

    @staticmethod
    def StandardSortDirectionQuery(description="Направление сортировки (asc/desc)"):
        return Query(
            default="asc",
            regex="^(asc|desc)$",
            description=description,
        )

    @staticmethod
    def StandardOptionalIntegerQuery(description="Опциональное числовое значение"):
        return Query(
            default=None,
            gt=0,
            description=description,
        )

    @staticmethod
    def StandardBooleanQuery(description="Логическое значение"):
        return Query(
            default=False,
            description=description,
        )

    @staticmethod
    def StandardOptionalBooleanQuery(description="Опциональное логическое значение"):
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardOptionalStringQuery(description="Опциональная строка"):
        return Query(
            default=None,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardOptionalIINQuery(description="Опциональная строка ИИН"):
        return Query(
            default=None,
            pattern=app_validation.IIN_REGEX,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardOptionalBINQuery(description="Опциональная строка БИН"):
        return Query(
            default=None,
            pattern=app_validation.BIN_REGEX,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardStringQuery(description="Обязательная строка"):
        return Query(
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardStringArrayQuery(description="Массив строк"):
        return Query(
            default=[],
            description=description,
        )

    @staticmethod
    def StandardOptionalStringArrayQuery(description="Опциональный массив строк"):
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardIntegerArrayQuery(description="Массив чисел"):
        return Query(
            default=[],
            description=description,
        )

    @staticmethod
    def StandardOptionalIntegerArrayQuery(description="Опциональный массив чисел"):
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardOptionalDateForScheduleQuery(description="Опциональный дата"):
        return Query(
            ge=app_config.get_scheduled_date_from_now().isoformat(),
            le=app_config.get_max_scheduled_date_from_now().isoformat(),
            default=app_config.get_scheduled_date_from_now().isoformat(),
            description=description,
        )
