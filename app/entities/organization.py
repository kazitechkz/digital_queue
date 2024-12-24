from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class OrganizationModel(Base):
    __tablename__ = AppTableNames.OrganizationTableName
    id: Mapped[DbColumnConstants.ID]
    full_name: Mapped[DbColumnConstants.StandardText]
    short_name: Mapped[DbColumnConstants.StandardText]
    bin: Mapped[DbColumnConstants.StandardUniqueBIN]
    bik: Mapped[DbColumnConstants.StandardNullableVarchar]
    kbe: Mapped[DbColumnConstants.StandardNullableVarchar]
    email: Mapped[DbColumnConstants.StandardUniqueEmail]
    phone: Mapped[DbColumnConstants.StandardUniquePhone]
    address: Mapped[DbColumnConstants.StandardNullableText]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.UserTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    type_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.OrganizationTypeTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
