from typing import Optional, List
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant
from app.adapters.dto.user.user_dto import UserRDTO
from app.adapters.dto.organization.organization_dto import OrganizationRDTO
from app.adapters.dto.vehicle.vehicle_dto import VehicleRDTO
from app.adapters.dto.order.order_dto import OrderRDTO
from app.adapters.dto.workshop_schedule.workshop_schedule_dto import WorkshopScheduleRDTO


# Базовый DTO
class ScheduleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True  # Привязка атрибутов модели SQLAlchemy


# DTO для чтения данных (без отношений)
class ScheduleRDTO(ScheduleDTO):
    order_id:DTOConstant.StandardNullableIntegerField()
    zakaz:DTOConstant.StandardNullableVarcharField()

    owner_id:DTOConstant.StandardNullableIntegerField()
    owner_name:DTOConstant.StandardVarcharField()
    owner_iin:DTOConstant.StandardVarcharField()
    owner_sid:DTOConstant.StandardNullableVarcharField()

    driver_id:DTOConstant.StandardNullableIntegerField()
    driver_name:DTOConstant.StandardVarcharField()
    driver_iin:DTOConstant.StandardVarcharField()
    driver_sid:DTOConstant.StandardNullableVarcharField()

    organization_id:DTOConstant.StandardNullableIntegerField()
    organization_full_name: DTOConstant.StandardNullableVarcharField()
    organization_bin: DTOConstant.StandardNullableVarcharField()

    vehicle_id:DTOConstant.StandardNullableIntegerField()
    vehicle_info:DTOConstant.StandardVarcharField()

    trailer_id:DTOConstant.StandardNullableIntegerField()
    trailer_info: DTOConstant.StandardNullableVarcharField()
    car_number: DTOConstant.StandardNullableVarcharField()

    workshop_schedule_id:DTOConstant.StandardNullableIntegerField()
    current_operation_id:DTOConstant.StandardNullableIntegerField()
    current_operation_name: DTOConstant.StandardNullableVarcharField()
    current_operation_value: DTOConstant.StandardNullableVarcharField()

    start_at:DTOConstant.StandardDateTimeField()
    end_at:DTOConstant.StandardDateTimeField()
    rescheduled_start_at:DTOConstant.StandardNullableDateTimeField()
    rescheduled_end_at:DTOConstant.StandardNullableDateTimeField()

    loading_volume: DTOConstant.StandardPriceField()
    loading_volume_kg: DTOConstant.StandardIntegerField()
    vehicle_tara: DTOConstant.StandardPriceField()
    vehicle_netto: DTOConstant.StandardPriceField()
    vehicle_brutto: DTOConstant.StandardPriceField()
    vehicle_tara_kg: DTOConstant.StandardIntegerField()
    vehicle_netto_kg: DTOConstant.StandardIntegerField()
    vehicle_brutto_kg: DTOConstant.StandardIntegerField()

    responsible_id:DTOConstant.StandardNullableIntegerField()
    responsible_name:DTOConstant.StandardNullableVarcharField()

    is_active:DTOConstant.StandardBooleanTrueField()
    is_used:DTOConstant.StandardBooleanFalseField()
    is_canceled:DTOConstant.StandardBooleanFalseField()
    is_executed:DTOConstant.StandardBooleanFalseField()
    executed_at:DTOConstant.StandardNullableDateTimeField()

    canceled_by: DTOConstant.StandardNullableIntegerField()
    canceled_by_name:DTOConstant.StandardNullableVarcharField()
    canceled_by_sid:DTOConstant.StandardNullableVarcharField()
    cancel_reason:DTOConstant.StandardNullableTextField()
    canceled_at:DTOConstant.StandardNullableDateTimeField()

    created_at:DTOConstant.StandardCreatedAt
    updated_at:DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class ScheduleCDTO(BaseModel):
    order_id:DTOConstant.StandardIntegerField()
    zakaz:DTOConstant.StandardVarcharField()

    owner_id:DTOConstant.StandardIntegerField()
    owner_name:DTOConstant.StandardVarcharField()
    owner_iin:DTOConstant.StandardVarcharField()
    owner_sid:DTOConstant.StandardVarcharField()

    driver_id:DTOConstant.StandardIntegerField()
    driver_name:DTOConstant.StandardVarcharField()
    driver_iin:DTOConstant.StandardVarcharField()
    driver_sid:DTOConstant.StandardVarcharField()

    organization_id:DTOConstant.StandardNullableIntegerField()
    organization_full_name: DTOConstant.StandardNullableVarcharField()
    organization_bin: DTOConstant.StandardNullableVarcharField()

    vehicle_id:DTOConstant.StandardIntegerField()
    vehicle_info:DTOConstant.StandardVarcharField()

    trailer_id:DTOConstant.StandardNullableIntegerField()
    trailer_info: DTOConstant.StandardNullableVarcharField()
    car_number: DTOConstant.StandardVarcharField()

    workshop_schedule_id:DTOConstant.StandardIntegerField()
    current_operation_id:DTOConstant.StandardIntegerField()
    current_operation_name: DTOConstant.StandardVarcharField()
    current_operation_value: DTOConstant.StandardVarcharField()

    start_at:DTOConstant.StandardDateTimeField()
    end_at:DTOConstant.StandardNullableDateTimeField()
    rescheduled_start_at:DTOConstant.StandardNullableDateTimeField()
    rescheduled_end_at:DTOConstant.StandardNullableDateTimeField()

    loading_volume: DTOConstant.StandardPriceField()
    vehicle_tara: DTOConstant.StandardPriceField()
    vehicle_netto: DTOConstant.StandardPriceField()
    vehicle_brutto: DTOConstant.StandardPriceField()

    responsible_id:DTOConstant.StandardNullableIntegerField()
    responsible_name:DTOConstant.StandardNullableVarcharField()

    is_active:DTOConstant.StandardBooleanTrueField()
    is_used:DTOConstant.StandardBooleanFalseField()
    is_canceled:DTOConstant.StandardBooleanFalseField()
    is_executed:DTOConstant.StandardBooleanFalseField()
    executed_at:DTOConstant.StandardNullableDateTimeField()

    canceled_by: DTOConstant.StandardNullableIntegerField()
    canceled_by_name:DTOConstant.StandardNullableVarcharField()
    canceled_by_sid:DTOConstant.StandardNullableVarcharField()
    cancel_reason:DTOConstant.StandardNullableTextField()
    canceled_at:DTOConstant.StandardNullableDateTimeField()


    class Config:
        from_attributes = True


class ScheduleWithRelationsDTO(ScheduleRDTO):
    owner: Optional[UserRDTO] = None
    driver: Optional[UserRDTO] = None
    organization: Optional[OrganizationRDTO] = None
    vehicle: Optional[VehicleRDTO] = None
    trailer: Optional[VehicleRDTO] = None
    order: Optional[OrderRDTO] = None
    # workshop_schedule: Optional[WorkshopScheduleRDTO] = None

    class Config:
        from_attributes = True
