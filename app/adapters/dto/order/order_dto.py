from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.factory.factory_dto import FactoryRDTO
from app.adapters.dto.material.material_dto import MaterialRDTO
from app.adapters.dto.order_status.order_status_dto import OrderStatusRDTO
from app.adapters.dto.organization.organization_dto import OrganizationRDTO
from app.adapters.dto.sap.sap_request_dto import SapRequestRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.adapters.dto.workshop.workshop_dto import WorkshopRDTO
from app.shared.dto_constants import DTOConstant


class OrderDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True

class OrderCDTO(BaseModel):
    status_id:DTOConstant.StandardIntegerField()
    status:DTOConstant.StandardVarcharField()
    factory_id: DTOConstant.StandardIntegerField()
    factory_sap_id: DTOConstant.StandardVarcharField()
    workshop_id: DTOConstant.StandardIntegerField()
    workshop_sap_id: DTOConstant.StandardVarcharField()
    material_id: DTOConstant.StandardIntegerField()
    material_sap_id: DTOConstant.StandardVarcharField()
    quan:DTOConstant.StandardIntegerField()
    quan_released:DTOConstant.StandardIntegerField()
    quan_booked:DTOConstant.StandardIntegerField()
    executed_cruise:DTOConstant.StandardNullableIntegerField()
    price_without_taxes:DTOConstant.StandardPriceField()
    price_with_taxes:DTOConstant.StandardPriceField()
    sap_id:DTOConstant.StandardNullableIntegerField()
    zakaz:DTOConstant.StandardNullableVarcharField()
    kaspi_id:DTOConstant.StandardNullableIntegerField()
    txn_id:DTOConstant.StandardNullableVarcharField()
    owner_id:DTOConstant.StandardIntegerField()
    iin:DTOConstant.StandardNullableVarcharField()
    owner_username:DTOConstant.StandardNullableVarcharField()
    owner_email:DTOConstant.StandardNullableVarcharField()
    owner_mobile:DTOConstant.StandardNullableVarcharField()
    name:DTOConstant.StandardNullableVarcharField()
    adr_index:DTOConstant.StandardNullableVarcharField()
    adr_city:DTOConstant.StandardNullableVarcharField()
    adr_str:DTOConstant.StandardNullableVarcharField()
    adr_dom:DTOConstant.StandardNullableVarcharField()
    organization_id:DTOConstant.StandardNullableIntegerField()
    bin:DTOConstant.StandardNullableVarcharField()
    dogovor:DTOConstant.StandardNullableVarcharField()
    is_active:DTOConstant.StandardBooleanTrueField()
    is_finished:DTOConstant.StandardBooleanFalseField()
    is_failed:DTOConstant.StandardBooleanFalseField()
    is_paid:DTOConstant.StandardBooleanFalseField()
    is_cancel:DTOConstant.StandardBooleanFalseField()
    start_at:DTOConstant.StandardCreatedAt
    end_at:DTOConstant.StandardNullableDateTimeField()
    finished_at:DTOConstant.StandardNullableDateTimeField()
    paid_at:DTOConstant.StandardNullableDateTimeField()
    cancel_at:DTOConstant.StandardNullableDateTimeField()
    canceled_by_user:DTOConstant.StandardNullableVarcharField()
    canceled_by_sid:DTOConstant.StandardNullableVarcharField()
    canceled_by_name:DTOConstant.StandardNullableVarcharField()
    checked_payment_by_id:DTOConstant.StandardNullableIntegerField()
    checked_payment_by:DTOConstant.StandardNullableVarcharField()
    checked_payment_at:DTOConstant.StandardNullableDateTimeField()
    payment_return_id:DTOConstant.StandardNullableIntegerField()

    class Config:
        from_attributes = True


class OrderRDTO(OrderDTO):
    status_id: DTOConstant.StandardNullableIntegerField()
    status: DTOConstant.StandardVarcharField()
    factory_id: DTOConstant.StandardNullableIntegerField()
    factory_sap_id: DTOConstant.StandardVarcharField()
    workshop_id: DTOConstant.StandardNullableIntegerField()
    workshop_sap_id: DTOConstant.StandardVarcharField()
    material_id: DTOConstant.StandardNullableIntegerField()
    material_sap_id: DTOConstant.StandardVarcharField()
    quan: DTOConstant.StandardIntegerField()
    quan_t: DTOConstant.StandardPriceField()
    quan_released: DTOConstant.StandardIntegerField()
    quan_released_t: DTOConstant.StandardPriceField()
    quan_booked: DTOConstant.StandardIntegerField()
    quan_booked_t: DTOConstant.StandardPriceField()
    quan_left: DTOConstant.StandardIntegerField()
    quan_left_t: DTOConstant.StandardPriceField()
    executed_cruise: DTOConstant.StandardNullableIntegerField()
    price_without_taxes: DTOConstant.StandardPriceField()
    price_with_taxes: DTOConstant.StandardPriceField()
    sap_id: DTOConstant.StandardNullableIntegerField()
    zakaz: DTOConstant.StandardNullableVarcharField()
    kaspi_id: DTOConstant.StandardNullableIntegerField()
    txn_id: DTOConstant.StandardNullableVarcharField()
    owner_id: DTOConstant.StandardNullableIntegerField()
    iin: DTOConstant.StandardNullableVarcharField()
    owner_sid: DTOConstant.StandardNullableVarcharField()
    owner_username: DTOConstant.StandardNullableVarcharField()
    owner_email: DTOConstant.StandardNullableVarcharField()
    owner_mobile: DTOConstant.StandardNullableVarcharField()
    name: DTOConstant.StandardNullableVarcharField()
    adr_index: DTOConstant.StandardNullableVarcharField()
    adr_city: DTOConstant.StandardNullableVarcharField()
    adr_str: DTOConstant.StandardNullableVarcharField()
    adr_dom: DTOConstant.StandardNullableVarcharField()
    organization_id: DTOConstant.StandardNullableIntegerField()
    bin: DTOConstant.StandardNullableVarcharField()
    dogovor: DTOConstant.StandardNullableVarcharField()
    is_active: DTOConstant.StandardBooleanTrueField()
    is_finished: DTOConstant.StandardBooleanFalseField()
    is_failed: DTOConstant.StandardBooleanFalseField()
    is_paid: DTOConstant.StandardBooleanFalseField()
    is_cancel: DTOConstant.StandardBooleanFalseField()
    start_at: DTOConstant.StandardCreatedAt
    end_at: DTOConstant.StandardNullableDateTimeField()
    finished_at: DTOConstant.StandardNullableDateTimeField()
    paid_at: DTOConstant.StandardNullableDateTimeField()
    cancel_at: DTOConstant.StandardNullableDateTimeField()
    must_paid_at: DTOConstant.StandardNullableDateTimeField()
    canceled_by_user: DTOConstant.StandardNullableIntegerField()
    canceled_by_sid: DTOConstant.StandardNullableVarcharField()
    canceled_by_name: DTOConstant.StandardNullableVarcharField()
    checked_payment_by_id: DTOConstant.StandardNullableIntegerField()
    checked_payment_by: DTOConstant.StandardNullableVarcharField()
    checked_payment_at: DTOConstant.StandardNullableDateTimeField()
    payment_return_id: DTOConstant.StandardNullableIntegerField()

    class Config:
        from_attributes = True

class OrderWithRelationsDTO(OrderRDTO):
    factory:Optional[FactoryRDTO] = None
    workshop:Optional[WorkshopRDTO] = None
    material:Optional[MaterialRDTO] = None
    sap:Optional[SapRequestRDTO] = None
    #kaspi:Optional[KaspiPaymentRDTO] = None
    owner:Optional[UserRDTO] = None
    organization:Optional[OrganizationRDTO] = None
    canceled_by:Optional[UserRDTO] = None
    checked_payment_by:Optional[UserRDTO] = None
    order_status:Optional[OrderStatusRDTO] = None
    #payment_return:Optional[PaymentReturnRDTO] = None