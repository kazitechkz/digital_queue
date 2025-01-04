from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


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

    # Relations
    organization: Mapped[AppModelNames.OrganizationModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.OrganizationModelName,
            back_populates="organization_employees",
            foreign_keys=f"{AppModelNames.OrganizationEmployeeModelName}.organization_id",
        )
    )
    employee: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="organization_employees",
        foreign_keys=f"{AppModelNames.OrganizationEmployeeModelName}.employee_id",
    )
    request: Mapped[AppModelNames.EmployeeRequestModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.EmployeeRequestModelName,
            back_populates="organization_employees",
            foreign_keys=f"{AppModelNames.OrganizationEmployeeModelName}.request_id",
        )
    )
