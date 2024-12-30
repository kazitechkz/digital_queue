from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class PaymentDocumentModel(Base):
    __tablename__ = AppTableNames.PaymentDocumentTableName

    id: Mapped[DbColumnConstants.ID]
    file_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.FileTableName, onupdate="cascade", ondelete="restrict"
        )
    ]
    order_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.OrderTableName, onupdate="cascade", ondelete="restrict"
        )
    ]
    checked_by: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    status: Mapped[DbColumnConstants.StandardBooleanNullable]
    comment: Mapped[DbColumnConstants.StandardNullableText]
    checked_at: Mapped[DbColumnConstants.StandardNullableDateTime]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    # Relationships
    order: Mapped[AppModelNames.OrderModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.OrderModelName,
        back_populates="payment_documents",
        foreign_keys=f"{AppModelNames.PaymentDocumentModelName}.order_id",
    )
    file: Mapped[AppModelNames.FileModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.FileModelName,
        back_populates="payment_documents",
        foreign_keys=f"{AppModelNames.PaymentDocumentModelName}.file_id",
    )
    checked_by_user: Mapped[AppModelNames.UserModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.UserModelName,
            back_populates="payment_documents",
            foreign_keys=f"{AppModelNames.PaymentDocumentModelName}.checked_by",
        )
    )
