from datetime import datetime
from typing import Optional

from sqlalchemy import Computed, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants, DbModelValue


class OrderModel(Base):
    __tablename__ = AppTableNames.OrderTableName

    id: Mapped[DbColumnConstants.ID]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderStatusTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    status: Mapped[DbColumnConstants.StandardVarcharIndex]
    factory_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FactoryTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    factory_sap_id: Mapped[DbColumnConstants.StandardVarcharIndex]

    workshop_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.WorkshopTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    workshop_sap_id: Mapped[DbColumnConstants.StandardVarcharIndex]

    material_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.MaterialTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    material_sap_id: Mapped[DbColumnConstants.StandardVarcharIndex]

    quan_t: Mapped[DbColumnConstants.StandardPrice]
    quan: Mapped[
        DbColumnConstants.StandardComputedInteger(
            table_exp=DbModelValue().quan, is_persisted=True
        )
    ]
    quan_released: Mapped[DbColumnConstants.StandardIntegerDefaultZero]
    quan_released_t: Mapped[
        DbColumnConstants.StandardComputedFloat(
            table_exp=DbModelValue().quan_released_t, is_persisted=True
        )
    ]
    quan_booked: Mapped[DbColumnConstants.StandardIntegerDefaultZero]
    quan_booked_t: Mapped[
        DbColumnConstants.StandardComputedFloat(
            table_exp=DbModelValue().quan_booked_t, is_persisted=True
        )
    ]
    quan_left: Mapped[
        DbColumnConstants.StandardComputedInteger(
            table_exp=DbModelValue().quan_left, is_persisted=True
        )
    ]
    quan_left_t: Mapped[
        DbColumnConstants.StandardComputedFloat(
            table_exp=DbModelValue().quan_left_t, is_persisted=True
        )
    ]

    executed_cruise: Mapped[DbColumnConstants.StandardIntegerDefaultZero]
    price_without_taxes: Mapped[DbColumnConstants.StandardPrice]
    price_with_taxes: Mapped[DbColumnConstants.StandardPrice]

    sap_id: Mapped[Optional[int]] = DbColumnConstants.ForeignKeyNullableInteger(
        AppTableNames.SAPRequestTableName, onupdate="cascade", ondelete="set null"
    )
    zakaz: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    kaspi_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.KaspiPaymentsTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    txn_id: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    iin: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    owner_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    owner_username: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    owner_email: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    owner_mobile: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    name: Mapped[DbColumnConstants.StandardNullableVarchar]
    adr_index: Mapped[DbColumnConstants.StandardNullableVarchar]
    adr_city: Mapped[DbColumnConstants.StandardNullableVarchar]
    adr_str: Mapped[DbColumnConstants.StandardNullableVarchar]
    adr_dom: Mapped[DbColumnConstants.StandardNullableVarchar]

    organization_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrganizationTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    bin: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    dogovor: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_finished: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_failed: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_cancel: Mapped[DbColumnConstants.StandardBooleanFalse]

    start_at: Mapped[DbColumnConstants.CreatedAt]
    end_at: Mapped[DbColumnConstants.StandardDateTime]
    finished_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    paid_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    cancel_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    must_paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(),
        Computed(DbModelValue().tomorrow, persisted=True),
        nullable=True,
    )

    canceled_by_user: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    canceled_by_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    canceled_by_name: Mapped[DbColumnConstants.StandardNullableVarchar]

    checked_payment_by_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    checked_payment_by: Mapped[DbColumnConstants.StandardNullableVarchar]
    checked_payment_at: Mapped[DbColumnConstants.StandardNullableDateTime]

    payment_return_id: Mapped[Optional[int]] = (
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentReturnTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    )

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
