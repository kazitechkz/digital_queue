from datetime import date, datetime, time
from typing import Annotated, Optional

from pydantic import EmailStr, Field

from app.shared.field_constants import FieldConstants
from app.shared.validation_constants import app_validation


class DTOConstant:
    @staticmethod
    def StandardID(description="Уникальный идентификатор"):
        return Annotated[int, Field(description=description)]

    @staticmethod
    def StandardTitleField(description="Наименование"):
        return Annotated[
            str,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description,
            ),
        ]

    @staticmethod
    def StandardUniqueValueField(description=None):
        return Annotated[
            str,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description
                or f"Уникальное значение длиной {FieldConstants.STANDARD_LENGTH}",
            ),
        ]

    @staticmethod
    def StandardVarcharField(description=None):
        return Annotated[
            str,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description
                or f"Строковое поле до {FieldConstants.STANDARD_LENGTH} символов",
            ),
        ]

    @staticmethod
    def StandardNullableVarcharField(description=None):
        return Annotated[
            Optional[str],
            Field(
                default=None,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description
                or f"Строковое поле до {FieldConstants.STANDARD_LENGTH} символов",
            ),
        ]

    @staticmethod
    def StandardIntegerField(description=None):
        return Annotated[
            int,
            Field(
                description=description or f"Числовое поле",
            ),
        ]

    @staticmethod
    def StandardNullableIntegerField(description=None):
        return Annotated[
            Optional[int],
            Field(
                default=None,
                nullable=True,
                description=description or f"Опциональное числовое поле",
            ),
        ]

    @staticmethod
    def StandardUnsignedIntegerField(description=None):
        return Annotated[
            int,
            Field(
                ge=0,
                description=description or f"Числовое поле",
            ),
        ]

    @staticmethod
    def StandardNullableUnsignedIntegerField(description=None):
        return Annotated[
            Optional[int],
            Field(
                default=None,
                ge=0,
                nullable=True,
                description=description or f"Опциональное числовое поле",
            ),
        ]

    @staticmethod
    def StandardEmailField(description=None):
        return Annotated[
            EmailStr,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or "Уникальный адрес электронной почты",
            ),
        ]

    @staticmethod
    def StandardPhoneField(description=None):
        return Annotated[
            str,
            Field(
                pattern=app_validation.KZ_MOBILE_REGEX,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or "Уникальный адрес электронной почты",
            ),
        ]

    @staticmethod
    def StandardCarNumberField(description=None):
        return Annotated[
            str,
            Field(
                pattern=app_validation.CAR_NUMBER_REGEX,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or "Уникальный номер автотранспорта 00XX(X)00",
            ),
        ]

    @staticmethod
    def StandardBooleanTrueField(description="Флаг активности (по умолчанию True)"):
        return Annotated[bool, Field(default=True, description=description)]

    @staticmethod
    def StandardBooleanFalseField(description="Флаг активности (по умолчанию False)"):
        return Annotated[bool, Field(default=False, description=description)]

    @staticmethod
    def StandardNullableBooleanField(description="Флаг активности"):
        return Annotated[Optional[bool], Field(description=description, default=None)]

    @staticmethod
    def StandardPriceField(description=None):
        return Annotated[
            float,
            Field(
                ge=0,
                description=description
                or f"Цена должна быть больше 0. Длина до {FieldConstants.PRICE_PRECISION} знаков",
            ),
        ]

    @staticmethod
    def StandardNullablePriceField(description=None):
        return Annotated[
            Optional[float],
            Field(
                default=None,
                ge=0,
                description=description
                or f"Опциональная цена больше 0. Длина до {FieldConstants.PRICE_PRECISION} знаков",
            ),
        ]

    @staticmethod
    def StandardDateField(description="Дата"):
        return Annotated[date, Field(description=description)]

    @staticmethod
    def StandardNullableDateField(description="Опциональная дата"):
        return Annotated[Optional[date], Field(default=None, description=description)]

    @staticmethod
    def StandardTimeField(description="Время"):
        return Annotated[time, Field(description=description)]

    @staticmethod
    def StandardNullableTimeField(description="Опциональная время"):
        return Annotated[Optional[time], Field(default=None, description=description)]

    @staticmethod
    def StandardDateTimeField(description="Дата и время"):
        return Annotated[datetime, Field(description=description)]

    @staticmethod
    def StandardNullableDateTimeField(description="Опциональная дата и время"):
        return Annotated[
            Optional[datetime], Field(default=None, description=description)
        ]

    @staticmethod
    def StandardNullableIINField(description="Уникальный идентификатор ИИН"):
        return Annotated[
            Optional[str],
            Field(
                nullable=True,
                pattern=app_validation.IIN_REGEX_STR,
                description=description or "Уникальный 12-значный ИИН",
            ),
        ]

    @staticmethod
    def StandardUniqueIINField(description="Уникальный идентификатор ИИН"):
        return Annotated[
            str,
            Field(
                pattern=app_validation.IIN_REGEX_STR,
                description=description or "Уникальный 12-значный ИИН",
            ),
        ]

    @staticmethod
    def StandardUniqueBINField(description="Уникальный идентификатор БИН"):
        return Annotated[
            str,
            Field(
                pattern=app_validation.BIN_REGEX_STR,
                description=description or "Уникальный 12-значный БИН",
            ),
        ]

    @staticmethod
    def StandardTextField(description="Текстовое описание"):
        return Annotated[str, Field(description=description)]

    @staticmethod
    def StandardNullableTextField(description="Опциональное текстовое описание"):
        return Annotated[Optional[str], Field(default=None, description=description)]

    StandardCreatedAt = Annotated[
        datetime, Field(description="Дата создания", example="2024-01-01T12:00:00")
    ]

    StandardUpdatedAt = Annotated[
        datetime, Field(description="Дата обновления", example="2024-01-01T12:00:00")
    ]
