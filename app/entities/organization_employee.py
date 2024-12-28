from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class OrganizationEmployeeModel(Base):
    __tablename__ = AppTableNames.OrganizationEmployeeTableName

    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]
    # Идентификатор организации
    organization_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.OrganizationTableName,
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    ]
    bin: Mapped[DbColumnConstants.StandardVarcharIndex]
    # Идентификатор сотрудника
    employee_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName,
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    ]
    sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    # Таймстампы создания и обновления
    request_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.EmployeeRequestTableName,
            ondelete="SET NULL",
            onupdate="CASCADE",
        )
    ]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    #Relations
