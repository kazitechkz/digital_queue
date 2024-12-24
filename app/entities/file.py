from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class FileModel(Base):
    __tablename__ = AppTableNames.FileTableName
    id: Mapped[DbColumnConstants.ID]
    filename: Mapped[DbColumnConstants.StandardVarchar]
    file_path: Mapped[DbColumnConstants.StandardText]
    file_size: Mapped[DbColumnConstants.StandardInteger]
    content_type: Mapped[DbColumnConstants.StandardVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
