from datetime import datetime, date, time
from typing import Annotated, Optional

from sqlalchemy import (
    text,
    String,
    Text,
    Numeric,
    Date,
    Integer,
    Boolean,
    ForeignKey,
    Computed,
    DateTime,
    Time,
)
from sqlalchemy.orm import mapped_column

from app.infrastructure.config import app_config
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


class DbModelValue:
    # quan
    @property
    def get_quan(self) -> str:
        if app_config.app_database == "postgresql":
            return "(quan_t * 1000)::INTEGER"
        return "CAST(quan_t * 1000 AS SIGNED)"

    @property
    def get_quan_release_t(self) -> str:
        if app_config.app_database == "postgresql":
            return "(quan_released / 1000.0)::FLOAT8"
        return "(quan_released / 1000.0)"

    @property
    def get_quan_booked_t(self) -> str:
        if app_config.app_database == "postgresql":
            return "quan_booked / 1000.0)::FLOAT8"
        return "(quan_booked  / 1000.0)"

    @property
    def get_quan_left(self) -> str:
        if app_config.app_database == "postgresql":
            return "(quan_t * 1000)::INTEGER - quan_booked - quan_released"
        return "CAST(quan_t * 1000 AS SIGNED) - quan_booked - quan_released"

    @property
    def get_quan_left_t(self) -> str:
        if app_config.app_database == "postgresql":
            return "((quan_t * 1000)::INTEGER - quan_booked - quan_released) / 1000.0"
        return "(CAST(quan_t * 1000 AS SIGNED) - quan_booked - quan_released) / 1000.0"

    @property
    def get_tomorrow(self) -> str:
        if app_config.app_database == "postgresql":
            return "(created_at + INTERVAL '1 day')"
        return "DATE_ADD(created_at, INTERVAL 1 DAY)"


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
    StandardNullableVarcharIndex = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), nullable=True, index=True
        ),
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
    StandardDateTime = Annotated[datetime, mapped_column(DateTime())]
    StandardNullableDateTime = Annotated[
        Optional[date], mapped_column(DateTime(), nullable=True)
    ]
    StandardNullableTime = Annotated[
        Optional[time], mapped_column(Time(), nullable=True)
    ]
    StandardTime = Annotated[time, mapped_column(Time())]
    StandardInteger = Annotated[int, mapped_column(Integer())]
    StandardIntegerDefaultZero = Annotated[int, mapped_column(Integer(), default=0)]
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

    # Вычисляемые столбцы для Integer
    StandardComputedInteger = lambda table_exp, is_persisted=None: Annotated[
        int,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            )
        ),
    ]

    StandardComputedNullableInteger = lambda table_exp, is_persisted=None: Annotated[
        Optional[int],
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            ),
            nullable=True,
        ),
    ]

    # Вычисляемые столбцы для Float
    StandardComputedFloat = lambda table_exp, is_persisted=None: Annotated[
        float,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            )
        ),
    ]

    StandardComputedNullableFloat = lambda table_exp, is_persisted=None: Annotated[
        Optional[float],
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            ),
            nullable=True,
        ),
    ]
