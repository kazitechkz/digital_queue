from datetime import datetime
from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sap.create_sap_order_dto import CreateLegalSapOrderDTO, CreateIndividualSapOrderDTO, SapStatusDTO
from app.adapters.dto.sap.sap_request_dto import SapRequestRDTO, SapRequestCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.sap_request.sap_request_repository import SapRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OrderModel
from app.infrastructure.api_clients.sap.sap_create_order_client import SapCreateOrderApiClient
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CreateClientSapOrderCase(BaseUseCase[SapRequestRDTO]):

    def __init__(self, db: AsyncSession):
        self.repository = SapRequestRepository(db)
        self.order_repository = OrderRepository(db)
        self.service = SapCreateOrderApiClient()

    async def execute(self,
                      order_id:int,
                      user:UserWithRelationsDTO,
                      ) -> SapRequestRDTO:
        order = await self.order_repository.get(id=order_id)
        await self.validate(order=order, user=user)
        sap_dto = await self.transform(order=order,user=user)
        create_sap_dto = self._create_sap_request_payload(order)
        response = await self.service.create_sap_order(create_sap_dto)
        dto = await self.transform(order=order,user=user,dto=sap_dto,response=response)
        model = await self.repository.create(obj=self.repository.model(**dto.dict()))
        if not model:
            raise AppExceptionResponse().internal_error(message="Произошла ошибка при создании заявки на создание заказа в SAP")
        return SapRequestRDTO.from_orm(model)


    async def validate(self, order:Optional[OrderModel], user: UserWithRelationsDTO):
        if not order:
            raise AppExceptionResponse.not_found(message="Заказ не найден")
        if order.sap_id or order.zakaz:
            raise AppExceptionResponse.bad_request(message="Заказ уже сформирован")
        if order.owner_id != user.id:
            raise AppExceptionResponse.bad_request(message="Заказ принадлежит не вам!")
        if order.status not in [AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS, AppDbValueConstants.INVOICE_CREATION_ERROR_STATUS]:
            raise AppExceptionResponse.bad_request(message="Заказ находится на другом этапе")

    async def transform(self,
                        order:OrderModel,
                        user: UserWithRelationsDTO,
                        dto:Optional[SapRequestCDTO] = None,
                        response:Optional[SapStatusDTO] = None
                        ) -> SapRequestCDTO:
        if not dto and not response:
            dto = SapRequestCDTO(
                order_id=order.id,
                werks=order.factory_sap_id,
                matnr=order.material_sap_id,
                kun_name=order.name,
                iin=order.iin,
                quan=order.quan_t,
                dogovor=order.dogovor,
                price=order.price_with_taxes,
                status=None,
                zakaz=None,
                text=None,
                pdf=None,
                date=None,
                time=None,
                is_active=False,
                is_failed=False,
                is_paid=False
            )
        elif dto and response:
            active_response = response.items[0]
            dto.status = f"{active_response.STATUS}"
            dto.zakaz = active_response.ZAKAZ
            dto.text = active_response.TEXT
            dto.pdf = active_response.PDF
            if active_response.DATE:
                dto.date = datetime.strptime(active_response.DATE, "%Y-%m-%d").date()
            if active_response.TIME:
                dto.time = datetime.strptime(active_response.TIME, "%H:%M:%S").time()
            if dto.zakaz:
                dto.is_active = True
                dto.is_failed = False
                dto.is_paid = False
        return dto


    def _create_sap_request_payload(self,model:OrderModel)->Union[CreateLegalSapOrderDTO, CreateIndividualSapOrderDTO]:
        if model.dogovor:
            return CreateLegalSapOrderDTO(
                DOGOVOR=model.dogovor,
                MATNR=model.material_sap_id,
                QUAN= model.quan_t,
                ORDER_ID = model.id
            )
        else:
            return CreateIndividualSapOrderDTO(
                WERKS = model.factory_sap_id,
                MATNR = model.material_sap_id,
                KUN_NAME = model.name,
                ADR_INDEX = model.adr_index,
                ADR_CITY = model.adr_city,
                ADR_STR = model.adr_str,
                ADR_DOM = model.adr_dom,
                IIN = model.iin,
                QUAN = model.quan_t,
                PRICE = model.price_with_taxes,
                ORDER_ID = model.id,
            )