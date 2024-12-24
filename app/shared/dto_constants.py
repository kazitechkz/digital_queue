from datetime import datetime
from typing import Annotated, Optional

from pydantic import Field

from app.shared.field_constants import FieldConstants


class DTOConstant:
    StandardID = Annotated[int, Field(description="Уникальный идентификатор")]

    StandardTitleRu = Annotated[
        str,
        Field(
            max_length=FieldConstants.STANDARD_LENGTH,
            description="Наименование на русском языке",
        ),
    ]

    StandardTitleKk = Annotated[
        str,
        Field(
            max_length=FieldConstants.STANDARD_LENGTH,
            description="Наименование на казахском языке",
        ),
    ]

    StandardTitleEn = Annotated[
        Optional[str],
        Field(
            max_length=FieldConstants.STANDARD_LENGTH,
            description="Наименование на английском языке",
        ),
    ]

    StandardValue = Annotated[
        str,
        Field(
            max_length=FieldConstants.STANDARD_LENGTH,
            description="Уникальное значение",
        ),
    ]

    StandardVarchar = Annotated[
        str,
        Field(
            max_length=FieldConstants.STANDARD_LENGTH,
            description="Строковое поле до 256 символов",
        ),
    ]

    StandardCreatedAt = Annotated[datetime, Field(description="Дата создания")]

    StandardUpdatedAt = Annotated[datetime, Field(description="Дата обновления")]
