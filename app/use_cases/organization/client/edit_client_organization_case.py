from typing import Optional

from fastapi import UploadFile
from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization.organization_dto import (
    OrganizationCDTO,
    OrganizationWithRelationsDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.organization.organization_repository import (
    OrganizationRepository,
)
from app.adapters.repositories.organization_type.organization_type_repository import (
    OrganizationTypeRepository,
)
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel, OrganizationModel
from app.infrastructure.config import app_config
from app.infrastructure.services.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class EditClientOrganizationCase(BaseUseCase[OrganizationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationRepository(db)
        self.organization_type_repository = OrganizationTypeRepository(db)
        self.user_repository = UserRepository(db)
        self.service = FileService(db)
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self,
        id: int,
        dto: OrganizationCDTO,
        user: UserWithRelationsDTO,
        file: Optional[UploadFile] = None,
    ) -> OrganizationWithRelationsDTO:
        file_model = None
        model = await self.validate(id=id, dto=dto, user=user)
        if AppFileExtensionConstants.is_upload_file(file):
            file_model = await self.service.save_file(
                file=file,
                uploaded_folder=AppFileExtensionConstants.OrganizationFolderName,
                extensions=self.extensions,
            )
        dto = await self.transform(dto=dto, file=file_model, model=model, user=user)
        model = await self.repository.update(obj=model, dto=dto)
        if not model:
            raise AppExceptionResponse().internal_error(
                message="Произошла ошибка при обновлении организации"
            )
        model = await self.repository.get(
            id=model.id,
            options=self.repository.default_relationships(),
        )
        return OrganizationWithRelationsDTO.from_orm(model)

    async def validate(
        self,
        id: int,
        dto: OrganizationCDTO,
        user: UserWithRelationsDTO,
    ) -> OrganizationModel:
        if dto.owner_id != user.id:
            raise AppExceptionResponse().bad_request(
                message="Укажите верного владельца"
            )
        model = await self.repository.get_first_with_filters(
            filters=[and_(self.repository.model.owner_id == dto.owner_id)]
        )
        if not model:
            raise AppExceptionResponse.not_found("Организация не найдена")
        verified_user = await self.user_repository.get_first_with_filters(
            filters=[or_(self.user_repository.model.id == dto.owner_id)],
            options=self.user_repository.default_relationships(),
        )
        if not verified_user:
            raise AppExceptionResponse().bad_request(
                message="Указанный владелец организации не найден"
            )
        if verified_user.user_type.value != AppDbValueConstants.LEGAL_VALUE:
            raise AppExceptionResponse().bad_request(
                message="Владелец организации должен быть юр. лицом"
            )
        existed_organization_type = await self.organization_type_repository.get(
            id=dto.type_id
        )
        if not existed_organization_type:
            raise AppExceptionResponse().bad_request(
                message="Тип организации не найден"
            )

        existed_organization = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    and_(
                        func.lower(self.repository.model.email) == dto.email.lower(),
                        self.repository.model.id != id,
                    ),
                    and_(
                        func.lower(self.repository.model.phone) == dto.phone.lower(),
                        self.repository.model.id != id,
                    ),
                    and_(
                        func.lower(self.repository.model.bin) == dto.bin.lower(),
                        self.repository.model.id != id,
                        self.repository.model.owner_id == user.id,
                    ),
                )
            ]
        )
        if existed_organization:
            detail: str = ""
            if existed_organization.bin.lower() == dto.bin.lower():
                detail = "БИН;"
            if existed_organization.phone.lower() == dto.phone.lower():
                detail = "Телефон;"
            if existed_organization.email.lower() == dto.email.lower():
                detail = "Почта;"
            raise AppExceptionResponse().bad_request(
                message=f"Организация с такими данными уже существует {detail}"
            )
        return model

    async def transform(
        self,
        dto: OrganizationCDTO,
        user: UserWithRelationsDTO,
        file: Optional[FileModel],
        model: OrganizationModel,
    ):
        if file:
            dto.file_id = file.id
        else:
            dto.file_id = model.file_id
        dto.owner_id = user.id
        if app_config.check_organization_by_moderator:
            dto.is_verified = False
        else:
            dto.is_verified = True
        return dto
