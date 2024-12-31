from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class FileDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FileCDTO(BaseModel):

    filename: DTOConstant.StandardVarcharField()
    file_path: DTOConstant.StandardTextField()
    file_size: DTOConstant.StandardIntegerField()
    content_type: DTOConstant.StandardVarcharField()

    class Config:
        from_attributes = True


class FileRDTO(FileDTO):
    filename: DTOConstant.StandardVarcharField()
    file_path: DTOConstant.StandardTextField()
    file_size: DTOConstant.StandardIntegerField()
    content_type: DTOConstant.StandardVarcharField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True
