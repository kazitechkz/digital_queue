from typing import Optional

from fastapi import UploadFile
from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle.vehicle_dto import VehicleCDTO, VehicleWithRelationsDTO
from app.adapters.repositories.organization.organization_repository import (
    OrganizationRepository,
)
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.adapters.repositories.vehicle_category.vehicle_category_repository import (
    VehicleCategoryRepository,
)
from app.adapters.repositories.vehicle_color.vehicle_color_repository import (
    VehicleColorRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileModel
from app.infrastructure.services.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CreateVehicleCase(BaseUseCase[VehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleRepository(db)
        self.vehicle_color_repository = VehicleColorRepository(db)
        self.vehicle_category_repository = VehicleCategoryRepository(db)
        self.user_repository = UserRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.service = FileService(db)
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: VehicleCDTO, file: Optional[UploadFile] = None
    ) -> VehicleWithRelationsDTO:
        await self.validate(dto)
        file_model = None
        if AppFileExtensionConstants.is_upload_file(file):
            file_model = await self.service.save_file(
                file=file,
                uploaded_folder=AppFileExtensionConstants.VehicleFolderName,
                extensions=self.extensions,
            )
        dto = await self.transform(dto=dto, file=file_model)
        model = await self.repository.create(obj=self.repository.model(**dto.dict()))
        if not model:
            raise AppExceptionResponse().internal_error(
                message="Произошла ошибка при создании транспорта"
            )
        model = await self.repository.get(
            id=model.id,
            options=self.repository.default_relationships(),
        )
        return VehicleWithRelationsDTO.from_orm(model)

    async def validate(self, dto: VehicleCDTO):
        if dto.owner_id:
            verified_user = await self.user_repository.get_first_with_filters(
                filters=[and_(self.user_repository.model.id == dto.owner_id)],
            )
            if not verified_user:
                raise AppExceptionResponse().bad_request(
                    message="Указанный владелец ТС не найден"
                )
        if dto.organization_id:
            verified_organization = (
                await self.organization_repository.get_first_with_filters(
                    filters=[
                        and_(
                            self.organization_repository.model.id == dto.organization_id
                        )
                    ],
                )
            )
            if not verified_organization:
                raise AppExceptionResponse().bad_request(
                    message="Указанная организация не найдена"
                )
        existed_vehicle_category = await self.vehicle_category_repository.get(
            id=dto.category_id
        )
        if not existed_vehicle_category:
            raise AppExceptionResponse().bad_request(message="Категория ТС не найдена")
        existed_vehicle_color = await self.vehicle_color_repository.get(id=dto.color_id)
        if not existed_vehicle_color:
            raise AppExceptionResponse().bad_request(message="Цвет ТС не найден")
        existed_vehicle = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.repository.model.registration_number)
                    == dto.registration_number.lower(),
                )
            ]
        )
        if existed_vehicle:
            raise AppExceptionResponse().bad_request(
                message=f"ТС с такими номерами уже существует"
            )

    async def transform(self, dto: VehicleCDTO, file: Optional[FileModel] = None):
        existed_vehicle_category = await self.vehicle_category_repository.get(
            id=dto.category_id
        )
        existed_vehicle_color = await self.vehicle_color_repository.get(id=dto.color_id)
        if file:
            dto.file_id = file.id
        dto.registration_number = dto.registration_number.upper()
        dto.vehicle_info = self.repository.get_vehicle_info(
            car_number=dto.registration_number,
            car_model=dto.car_model,
            car_color=existed_vehicle_color,
            car_category=existed_vehicle_category,
        )
        return dto
