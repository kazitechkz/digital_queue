from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class EmployeeRequestModel(Base):
    __tablename__ = AppTableNames.EmployeeRequestTableName

    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]

    # Организация
    organization_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.OrganizationTableName,
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    ]
    organization_full_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    organization_bin: Mapped[DbColumnConstants.StandardNullableVarchar]

    # Владелец
    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            ondelete="SET NULL",
            onupdate="CASCADE",
        )
    ]
    owner_name: Mapped[DbColumnConstants.StandardVarchar]
    owner_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    # Сотрудник
    employee_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName,
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    ]
    employee_name: Mapped[DbColumnConstants.StandardVarchar]
    employee_email: Mapped[DbColumnConstants.StandardVarchar]
    employee_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    # Статус
    status: Mapped[DbColumnConstants.StandardNullableInteger]  # -1 rejected, 1 approved

    # Даты запроса и решения
    requested_at: Mapped[DbColumnConstants.StandardDateTime]
    decided_at: Mapped[DbColumnConstants.StandardNullableDateTime]

    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    #Relations
    organization: Mapped[AppModelNames.OrganizationModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.OrganizationModelName,
        back_populates="employee_requests",
        foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.organization_id"
    )

    owner: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="sent_employee_requests",
        foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.owner_id"
    )
    employee: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="received_employee_requests",
        foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.employee_id"
    )