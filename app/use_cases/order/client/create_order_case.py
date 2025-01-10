from datetime import datetime
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.order.create_order_dto import CreateOrderDTO
from app.adapters.dto.order.order_dto import OrderWithRelationsDTO, OrderCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.material.material_repository import MaterialRepository
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.order_status.order_status_repository import OrderStatusRepository
from app.adapters.repositories.organization.organization_repository import OrganizationRepository
from app.adapters.repositories.sap_request.sap_request_repository import SapRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CreateClientOrderCase(BaseUseCase[OrderWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)
        self.material_repository = MaterialRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.order_status_repository = OrderStatusRepository(db)
        self.sap_request_repository = SapRequestRepository(db)

    async def execute(self,
                      dto: CreateOrderDTO,
                      user:UserWithRelationsDTO,
                      ) -> OrderWithRelationsDTO:
        await self.validate(dto,user)
        dto:OrderCDTO = await self.transform(dto=dto,user=user)
        model = await self.repository.create(obj=self.repository.model(**dto.dict()))
        if not model:
            raise AppExceptionResponse.internal_error("Ошибка создания заказа")
        model = await self.repository.get(id=model.id, options=self.repository.default_relationships())
        return OrderWithRelationsDTO.from_orm(model)


    async def validate(self, dto: CreateOrderDTO,user:UserWithRelationsDTO):
        #Если юр лицо проверяем принадлежит ли нам организация, активна ли и существует ли в целом
        if user.user_type.value == AppDbValueConstants.LEGAL_VALUE:
            if not dto.dogovor:
                raise AppExceptionResponse.bad_request("Введите номер договора SAP")
            if not dto.organization_id:
                raise AppExceptionResponse.bad_request("Введите организацию")
            organization = await self.organization_repository.get(id=dto.organization_id)
            if not organization:
                raise AppExceptionResponse.bad_request("Организация не найдена")
            if organization.owner_id != user.id:
                raise AppExceptionResponse.bad_request("Вы не являетесь владельцем этой организации")
            if app_config.check_organization_by_moderator:
                if not organization.is_verified:
                    raise AppExceptionResponse.bad_request("Организация не активна")
        #Проверяем наличие материала и тоннажа
        material = await self.material_repository.get_first_with_filters(
            filters=[and_(
                self.material_repository.model.status,
                func.lower(self.material_repository.model.sap_id) == dto.material_sap_id.lower()
            )]
        )
        if not material:
            raise AppExceptionResponse.bad_request("Материал не найден, либо не активен")

        if (dto.quan_t * 1000) < app_config.order_create_min_kg:
            raise AppExceptionResponse.bad_request(
                f"Минимальный тоннаж заказа {app_config.order_create_min_kg} кг, введено {dto.quan_t * 1000} кг"
            )


    async def transform(self, dto: CreateOrderDTO,user:UserWithRelationsDTO)->OrderCDTO:
        if user.user_type.value == AppDbValueConstants.INDIVIDUAL_VALUE:
            dto.organization_id = None
            dto.dogovor = None

        material = await self.material_repository.get_first_with_filters(
            filters=[and_(
                self.material_repository.model.status,
                func.lower(self.material_repository.model.sap_id) == dto.material_sap_id.lower()
            )],
            options=self.material_repository.default_relationships()
        )
        first_status = await self.order_status_repository.get_first_with_filters(
            filters=[and_(self.order_status_repository.model.value == AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS)]
        )
        if not material or not first_status:
            raise AppExceptionResponse.bad_request("Ошибка при создании заказа (Материал или статус)")
        bin = None
        organization_id = None
        if user.user_type.value == AppDbValueConstants.LEGAL_VALUE:
            for user_organization in user.organizations:
                if user_organization.id == dto.organization_id:
                    bin = user_organization.bin
                    organization_id = user_organization.id
                    break

        return OrderCDTO(
            status_id= first_status.id,
            status = first_status.value,
            factory_id = material.workshop.factory_id,
            factory_sap_id= material.workshop.factory_sap_id,
            workshop_id = material.workshop_id,
            workshop_sap_id = material.workshop_sap_id,
            material_id = material.id,
            material_sap_id = material.sap_id,
            quan = dto.quan_t * 1000,
            quan_released = 0,
            quan_booked = 0,
            executed_cruise = 0,
            price_without_taxes = float(material.price_without_taxes) * float(dto.quan_t),
            price_with_taxes = float(material.price_with_taxes) * float(dto.quan_t),
            sap_id = None,
            zakaz = None,
            kaspi_id = None,
            txn_id = None,
            owner_id = user.id,
            iin = user.iin,
            owner_sid = user.sid,
            owner_username = user.preferred_username,
            owner_email = user.email,
            owner_mobile = user.phone,
            name = user.name,
            adr_index = dto.adr_index,
            adr_city = dto.adr_city,
            adr_str = dto.adr_str,
            adr_dom = dto.adr_dom,
            organization_id = organization_id,
            bin = bin,
            dogovor = dto.dogovor,
            is_active = True,
            is_finished = False,
            is_failed = False,
            is_paid = False,
            is_cancel = False,
            start_at = datetime.now(),
            end_at = None,
            finished_at = None,
            paid_at = None,
            cancel_at = None,
            canceled_by_user = None,
            canceled_by_sid = None,
            canceled_by_name = None,
            checked_payment_by_id = None,
            checked_payment_by = None,
            checked_payment_at = None,
            payment_return_id = None,
        )
