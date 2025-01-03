from typing import Optional

from fastapi import UploadFile
from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserCDTO, UserWithRelationsDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.user_type.user_type_repository import \
    UserTypeRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_password_hash
from app.entities import FileModel, UserModel
from app.infrastructure.services.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_cases.base_case import BaseUseCase


class UpdateUserCase(BaseUseCase[UserWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
        self.user_type_repository = UserTypeRepository(db)
        self.service = FileService(db)
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(self,id:int, dto: UserCDTO,file:Optional[UploadFile] = None) -> UserWithRelationsDTO:
        model = await self.validate(id=id,dto=dto)
        file_model = None
        if AppFileExtensionConstants.is_upload_file(file):
            file_model = await self.service.save_file(
                file=file,
                uploaded_folder=AppFileExtensionConstants.UserFolderName,
                extensions=self.extensions,
            )
        dto = await self.transform(model=model,dto=dto,file=file_model)
        model = await self.repository.update(obj=model,dto=dto)
        if not model:
            raise AppExceptionResponse.internal_error(message="Ошибка при обновлении пользователя")
        model = await self.repository.get(
            id=model.id,
            options=self.repository.default_relationships(),
        )
        return UserWithRelationsDTO.from_orm(model)

    async def validate(self,id:int, dto: UserCDTO):
        model = await self.repository.get(id=id)
        if model is None:
            raise AppExceptionResponse.not_found("Пользователь не найден")
        existed = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    and_(func.lower(self.repository.model.iin) == dto.iin.lower(),self.repository.model.id != id),
                    and_(func.lower(self.repository.model.sid) == dto.sid.lower(),self.repository.model.id != id),
                    and_(func.lower(self.repository.model.preferred_username) == dto.preferred_username.lower(),self.repository.model.id != id),
                )
            ]
        )
        if existed:
            existed_column = ""
            if existed.iin.lower() == dto.iin.lower():
                existed_column += "ИИН;"
            if existed.sid.lower() == dto.sid.lower():
                existed_column += "Уникальный идентификатор KeyCloak;"
            if existed.preferred_username.lower() == dto.preferred_username.lower():
                existed_column += "Никнейм;"
            raise AppExceptionResponse.bad_request(
                f"Пользователь с такими данными уже существует:{existed_column}"
            )
        existed_role = await self.role_repository.get(id=dto.role_id)
        if not existed_role:
            raise AppExceptionResponse.bad_request("Роль не найдена")
        existed_user_type = await self.user_type_repository.get(id=dto.type_id)
        if not existed_user_type:
            raise AppExceptionResponse.bad_request("Тип пользователя не найден")
        return model

    async def transform(self,model:UserModel,dto:UserCDTO,file:Optional[FileModel] = None):
        if file is not None:
            dto.file_id = file.id
        else:
            dto.file_id = model.file_id
        if dto.password_hash:
            dto.password_hash = get_password_hash(dto.password_hash)
        else:
            dto.password_hash = model.password_hash
        return dto