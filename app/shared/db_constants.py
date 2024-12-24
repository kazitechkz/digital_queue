from datetime import datetime, date
from typing import Annotated, Optional

from sqlalchemy import text, String, Text, Numeric, Date, Integer, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.shared.field_constants import FieldConstants


class AppDbValueConstants:
    # roles
    ADMINISTRATOR_VALUE = "administrator"
    MODERATOR_VALUE = "moderator"
    COMPANY_LEAD_VALUE = "company_lead"
    COMPANY_MANAGER_VALUE = "company_manager"
    EMPLOYEE_VALUE = "employee"
    # Роли, которые нельзя удалить или изменить
    IMMUTABLE_ROLES = frozenset(
        [
            ADMINISTRATOR_VALUE,
            MODERATOR_VALUE,
            COMPANY_LEAD_VALUE,
            COMPANY_MANAGER_VALUE,
            EMPLOYEE_VALUE,
        ]
    )
    # Languages
    RUSSIAN_VALUE = "ru"
    KAZAKH_VALUE = "kk"
    ENGLISH_VALUE = "en"
    IMMUTABLE_LANGUAGES = frozenset(
        [
            RUSSIAN_VALUE,
            KAZAKH_VALUE,
            ENGLISH_VALUE,
        ]
    )
    # UserTypes
    INDIVIDUAL_VALUE = "individual"
    LEGAL_VALUE = "legal"
    IMMUTABLE_USER_TYPES = frozenset(
        [
            INDIVIDUAL_VALUE,
            LEGAL_VALUE,
        ]
    )
    # Organization Types
    LLP_VALUE = "llp"
    IE_VALUE = "ie"
    JCS_VALUE = "jcs"
    SC_VALUE = "sc"
    FE_VALUE = "fe"
    PC_VALUE = "pc"
    NON_JCS_VALUE = "non_jcs"
    IMMUTABLE_ORGANIZATION_TYPES = frozenset(
        [
            LLP_VALUE,
            IE_VALUE,
            JCS_VALUE,
            SC_VALUE,
            FE_VALUE,
            PC_VALUE,
            NON_JCS_VALUE,
        ]
    )


class DbColumnConstants:
    ID = Annotated[int, mapped_column(primary_key=True)]
    CreatedAt = Annotated[
        datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    ]
    UpdatedAt = Annotated[
        datetime,
        mapped_column(
            server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now()
        ),
    ]
    # Аннотации для стандартных типов
    StandardVarchar = Annotated[
        str, mapped_column(String(length=FieldConstants.STANDARD_LENGTH))
    ]
    StandardVarcharIndex = Annotated[
        str, mapped_column(String(length=FieldConstants.STANDARD_LENGTH), index=True)
    ]
    StandardNullableVarchar = Annotated[
        str, mapped_column(String(length=FieldConstants.STANDARD_LENGTH), nullable=True)
    ]
    StandardUniqueIIN = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.IIN_LENGTH), unique=True, index=True
        ),
    ]
    StandardUniqueBIN = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.BIN_LENGTH), unique=True, index=True
        ),
    ]
    StandardUniqueEmail = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=True, index=True
        ),
    ]
    StandardEmail = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=False, index=True
        ),
    ]
    StandardUniquePhone = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=True, index=True
        ),
    ]
    StandardPhone = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=False, index=True
        ),
    ]
    StandardUniqueValue = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=True, index=True
        ),
    ]
    StandardNullableText = Annotated[str, mapped_column(Text(), nullable=True)]
    StandardText = Annotated[str, mapped_column(Text())]
    StandardPrice = Annotated[
        float,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            )
        ),
    ]
    StandardNullablePrice = Annotated[
        Optional[float],
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            ),
            nullable=True,
        ),
    ]

    StandardNullableDate = Annotated[
        Optional[date], mapped_column(Date(), nullable=True)
    ]
    StandardDate = Annotated[date, mapped_column(Date())]

    StandardInteger = Annotated[int, mapped_column(Integer())]
    StandardNullableInteger = Annotated[
        Optional[int], mapped_column(Integer(), nullable=True)
    ]

    StandardBooleanTrue = Annotated[
        bool, mapped_column(Boolean(), nullable=False, default=True)
    ]
    StandardBooleanFalse = Annotated[
        bool, mapped_column(Boolean(), nullable=False, default=False)
    ]
    StandardBooleanNullable = Annotated[bool, mapped_column(Boolean(), nullable=True)]
    StandardBooleanNullableTrue = Annotated[
        bool, mapped_column(Boolean(), nullable=True, default=True)
    ]
    StandardBooleanNullableFalse = Annotated[
        bool, mapped_column(Boolean(), nullable=True, default=False)
    ]

    # ForeignKey унификации с onupdate и ondelete
    ForeignKeyInteger = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            int,
            mapped_column(
                Integer(),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=False,
            ),
        ]
    )
    ForeignKeyNullableInteger = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            Optional[int],
            mapped_column(
                Integer(),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=True,
            ),
        ]
    )

    ForeignKeyString = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            str,
            mapped_column(
                String(length=255),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=False,
            ),
        ]
    )
    ForeignKeyNullableString = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            Optional[str],
            mapped_column(
                String(length=255),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=True,
            ),
        ]
    )
