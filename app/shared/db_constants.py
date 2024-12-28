from datetime import date, datetime, time
from typing import Annotated, Optional

from sqlalchemy import (Boolean, Computed, Date, DateTime, ForeignKey, Integer,
                        Numeric, String, Text, Time, text)
from sqlalchemy.orm import mapped_column

from app.infrastructure.config import app_config
from app.shared.field_constants import FieldConstants


class AppDbValueConstants:
    # roles
    ADMINISTRATOR_VALUE = "administrator"
    ADMINISTRATOR_KEYCLOAK_VALUE = "administrator"

    SECURITY_VALUE = "security"
    SECURITY_KEYCLOAK_VALUE = "security"

    SECURITY_LOADER_VALUE = "security_loader"
    SECURITY_LOADER_KEYCLOAK_VALUE = "security_loader"

    LOADER_VALUE = "loader"
    LOADER_KEYCLOAK_VALUE = "loader"

    WEIGHER_VALUE = "weigher"
    WEIGHER_KEYCLOAK_VALUE = "weigher"

    MANAGER_VALUE = "manager"
    MANAGER_KEYCLOAK_VALUE = "manager"

    CLIENT_VALUE = "client"
    CLIENT_KEYCLOAK_VALUE = "client"
    # Роли, которые нельзя удалить или изменить
    IMMUTABLE_ROLES = frozenset(
        [
            ADMINISTRATOR_VALUE,
            SECURITY_VALUE,
            SECURITY_LOADER_VALUE,
            LOADER_VALUE,
            WEIGHER_VALUE,
            MANAGER_VALUE,
            CLIENT_VALUE,
        ]
    )

    # UserTypes
    INDIVIDUAL_VALUE = "individual"
    INDIVIDUAL_KEYCLOAK_VALUE = "individual"
    LEGAL_VALUE = "legal"
    LEGAL_KEYCLOAK_VALUE = "legal"
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
    # Order Status Values
    WAITING_FOR_INVOICE_CREATION_STATUS = "waiting_for_invoice_creation"
    INVOICE_CREATION_ERROR_STATUS = "invoice_creation_error"
    WAITING_FOR_PAYMENT_STATUS = "waiting_for_payment"
    WAITING_FOR_PAYMENT_CONFIRMATION_STATUS = "waiting_for_payment_confirmation"
    PAYMENT_REJECTED_STATUS = "payment_rejected"
    PAYMENT_CONFIRMATION_REJECTED_STATUS = "payment_confirmation_rejected"
    PAID_WAITING_FOR_BOOKING_STATUS = "paid_waiting_for_booking"
    IN_PROGRESS_STATUS = "in_progress"
    COMPLETED_STATUS = "completed"
    DECLINED_STATUS = "declined"
    IMMUTABLE_ORDER_STATUS = frozenset(
        [
            WAITING_FOR_INVOICE_CREATION_STATUS,
            INVOICE_CREATION_ERROR_STATUS,
            WAITING_FOR_PAYMENT_STATUS,
            WAITING_FOR_PAYMENT_CONFIRMATION_STATUS,
            PAYMENT_REJECTED_STATUS,
            PAYMENT_CONFIRMATION_REJECTED_STATUS,
            PAID_WAITING_FOR_BOOKING_STATUS,
            IN_PROGRESS_STATUS,
            COMPLETED_STATUS,
            DECLINED_STATUS,
        ]
    )

    # Operation Status Values
    VALIDATION_BEFORE_ENTRY = "validation_before_entry"
    ENTRY_CHECKPOINT = "entry_checkpoint"
    INITIAL_WEIGHING = "initial_weighing"
    VALIDATION_BEFORE_LOADING = "validation_before_loading"
    LOADING_GOODS = "loading_goods"
    CONTROL_WEIGHING = "control_weighing"
    EXIT_SECURITY_CHECKPOINT = "exit_security_checkpoint"
    SECURITY_VALIDATION_BEFORE_UNLOADING_AND_CANCELLATION = (
        "security_validation_before_unloading_and_cancellation"
    )
    UNLOADING_EXCESS_GOODS_AND_EXIT = "unloading_excess_goods_and_exit"
    SECURITY_VALIDATION_BEFORE_UNLOADING_AND_WEIGHING = (
        "security_validation_before_unloading_and_weighing"
    )
    UNLOADING_EXCESS_GOODS_AND_WEIGHING = "unloading_excess_goods_and_weighing"
    SUCCESSFULLY_COMPLETED = "successfully_completed"
    CANCELLED = "cancelled"


class DbModelValue:
    @property
    def is_postgresql(self) -> bool:
        """Проверяет, используется ли PostgreSQL как база данных."""
        return app_config.app_database.lower() == "postgresql"

    def to_kg(self, column_name) -> str:
        """Вычисление to_kg."""
        if self.is_postgresql:
            return f"({column_name} * 1000)::INTEGER"
        return f"CAST({column_name} * 1000 AS SIGNED)"

    @property
    def quan(self) -> str:
        """Вычисление QUAN."""
        if self.is_postgresql:
            return "(quan_t * 1000)::INTEGER"
        return "CAST(quan_t * 1000 AS SIGNED)"

    @property
    def quan_released_t(self) -> str:
        """Вычисление QUAN_RELEASED_T."""
        if self.is_postgresql:
            return "(quan_released / 1000.0)::DOUBLE PRECISION"
        return "(quan_released / 1000.0)"

    @property
    def quan_booked_t(self) -> str:
        """Вычисление QUAN_BOOKED_T."""
        if self.is_postgresql:
            return "(quan_booked / 1000.0)::DOUBLE PRECISION"
        return "(quan_booked / 1000.0)"

    @property
    def quan_left(self) -> str:
        """Вычисление QUAN_LEFT."""
        if self.is_postgresql:
            return "(quan_t * 1000)::INTEGER - quan_booked - quan_released"
        return "CAST(quan_t * 1000 AS SIGNED) - quan_booked - quan_released"

    @property
    def quan_left_t(self) -> str:
        """Вычисление QUAN_LEFT_T."""
        if self.is_postgresql:
            return "((quan_t * 1000)::INTEGER - quan_booked - quan_released) / 1000.0"
        return "(CAST(quan_t * 1000 AS SIGNED) - quan_booked - quan_released) / 1000.0"

    @property
    def tomorrow(self) -> str:
        """Вычисление TOMORROW."""
        if self.is_postgresql:
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


from sqlalchemy.orm import relationship


class DbRelationshipConstants:
    @staticmethod
    def one_to_many(
            target: str,
            back_populates: str,
            foreign_keys: str | list = None,
            cascade: str = "all",
            lazy: str = "select",
    ):
        """
        Унифицированное создание отношения один-ко-многим.

        Args:
            target (str): Целевая модель.
            back_populates (str): Связанное поле в целевой модели.
            foreign_keys (list): Список внешних ключей, если нужно.
            cascade (str): Стратегия каскадного удаления.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
        )

    @staticmethod
    def one_to_one(
            target: str,
            back_populates: str,
            foreign_keys: str|list = None,
            cascade: str = "all",
            lazy: str = "select",
    ):
        """
        Создает отношение один-к-одному.

        Args:
            target (str): Целевая модель.
            back_populates (str): Связанное поле в целевой модели.
            foreign_keys (list): Внешние ключи.
            cascade (str): Стратегия каскадирования.
            lazy (str): Стратегия загрузки данных.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
            uselist=False,  # Ключевой параметр для один-к-одному
        )

    @staticmethod
    def many_to_one(
            target: str,
            back_populates: str,
            foreign_keys: str|list = None,
            cascade: str = "all",
            lazy: str = "select",
    ):
        """
        Унифицированное создание отношения многие-к-одному.

        Args:
            target (str): Целевая модель.
            back_populates (str): Связанное поле в целевой модели.
            cascade (str): Стратегия каскадного удаления.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            back_populates=back_populates,
            cascade=cascade,
            lazy=lazy,
            foreign_keys=foreign_keys
        )

    @staticmethod
    def many_to_many(
            target: str,
            secondary: str,
            back_populates: str,
            cascade: str = "all",
            lazy: str = "select",
    ):
        """
        Унифицированное создание отношения многие-ко-многим.

        Args:
            target (str): Целевая модель.
            secondary (str): Связующая таблица для отношения многие-ко-многим.
            back_populates (str): Связанное поле в целевой модели.
            cascade (str): Стратегия каскадного удаления.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            secondary=secondary,
            back_populates=back_populates,
            cascade=cascade,
            lazy=lazy,
        )

    @staticmethod
    def self_referential(
        target: str,
        back_populates: str,
        foreign_keys: list|str = None,
        cascade: str = "save-update, merge",
        lazy: str = "select",
    ):
        """
        Creates a self-referential relationship.

        Args:
            target (str): The target model for the relationship.
            back_populates (str): The field in the target model to map back.
            foreign_keys (list): The foreign key(s) defining the relationship.
            cascade (str): Cascade behavior for the relationship.
            lazy (str): The loading strategy for the relationship.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Configured relationship.
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
        )

    @staticmethod
    def self_referential(
            target: str,
            foreign_keys: list|str,
            remote_side: str,
            lazy: str = "select",
    ):
        """
        Создаёт самоссылающееся отношение.

        Args:
            target (str): Имя целевой модели.
            foreign_keys (list): Внешние ключи для отношения.
            remote_side (str): Поле на удалённой стороне для установления связи.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            foreign_keys=foreign_keys,
            remote_side=remote_side,
            lazy=lazy,
        )
