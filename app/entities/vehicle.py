from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class VehicleModel(Base):
    __tablename__ = AppTableNames.VehicleTableName
    id: Mapped[DbColumnConstants.ID]
    category_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.VehicleCategoryTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]
    color_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.VehicleColorTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]

    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.UserTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]
    organization_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.OrganizationTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]
    registration_number: Mapped[DbColumnConstants.StandardVarchar]
    car_model: Mapped[DbColumnConstants.StandardVarchar]
    is_trailer: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
