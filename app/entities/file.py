from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class FileModel(Base):
    __tablename__ = AppTableNames.FileTableName
    id: Mapped[DbColumnConstants.ID]
    filename: Mapped[DbColumnConstants.StandardVarchar]
    file_path: Mapped[DbColumnConstants.StandardText]
    file_size: Mapped[DbColumnConstants.StandardInteger]
    content_type: Mapped[DbColumnConstants.StandardVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    factories: Mapped[List[AppModelNames.FactoryModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.FactoryModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.FactoryModelName}.file_id",
        )
    )
    materials: Mapped[List[AppModelNames.MaterialModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.MaterialModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.MaterialModelName}.file_id",
        )
    )
    organizations: Mapped[List[AppModelNames.OrganizationModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrganizationModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.OrganizationModelName}.file_id",
        )
    )
    payment_documents: Mapped[List[AppModelNames.PaymentDocumentModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.PaymentDocumentModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.PaymentDocumentModelName}.file_id",
        )
    )
    users: Mapped[List[AppModelNames.UserModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.UserModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.UserModelName}.file_id",
        )
    )
    vehicles: Mapped[List[AppModelNames.VehicleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.VehicleModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.VehicleModelName}.file_id",
        )
    )
    workshops: Mapped[List[AppModelNames.WorkshopModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.WorkshopModelName,
            back_populates="file",
            foreign_keys=f"{AppModelNames.WorkshopModelName}.file_id",
        )
    )
