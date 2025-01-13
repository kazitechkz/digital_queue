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
    zakaz: DTOConstant.StandardNullableVarcharField(description="Номер заказа")
    owner_name: DTOConstant.StandardVarcharField(description="Имя владельца")
    owner_iin: DTOConstant.StandardVarcharField(description="ИИН владельца")
    owner_sid: DTOConstant.StandardNullableVarcharField(description="SID владельца")
    driver_name: DTOConstant.StandardNullableVarcharField(description="Имя водителя")
    driver_iin: DTOConstant.StandardNullableVarcharField(description="ИИН водителя")
    driver_sid: DTOConstant.StandardNullableVarcharField(description="SID водителя")
    organization_full_name: DTOConstant.StandardNullableVarcharField(
        description="Полное название организации"
    )
    organization_bin: DTOConstant.StandardNullableVarcharField(
        description="БИН организации"
    )
    vehicle_info: DTOConstant.StandardTextField(
        description="Информация о транспортном средстве"
    )
    trailer_info: DTOConstant.StandardNullableTextField(
        description="Информация о прицепе"
    )
    car_number: DTOConstant.StandardNullableVarcharField(description="Номер автомобиля")
    start_at: DTOConstant.StandardDateTimeField(description="Начало расписания")
    end_at: DTOConstant.StandardDateTimeField(description="Конец расписания")
    rescheduled_start_at: DTOConstant.StandardNullableDateTimeField(
        description="Перенесенное время начала"
    )
    rescheduled_end_at: DTOConstant.StandardNullableDateTimeField(
        description="Перенесенное время конца"
    )
    loading_volume: DTOConstant.StandardPriceField(description="Объем загрузки")
    vehicle_tara: DTOConstant.StandardPriceField(
        description="Тара транспортного средства"
    )
    vehicle_netto: DTOConstant.StandardPriceField(description="Вес нетто")
    vehicle_brutto: DTOConstant.StandardPriceField(description="Вес брутто")
    responsible_name: DTOConstant.StandardNullableVarcharField(
        description="Имя ответственного лица"
    )
    is_active: DTOConstant.StandardBooleanTrueField(description="Активность расписания")
    is_used: DTOConstant.StandardBooleanFalseField(
        description="Использовано расписание"
    )
    is_canceled: DTOConstant.StandardBooleanFalseField(
        description="Отменено расписание"
    )
    is_executed: DTOConstant.StandardBooleanFalseField(
        description="Исполнено расписание"
    )

    class Config:
        from_attributes = True  # Привязка атрибутов модели SQLAlchemy


# DTO для создания/обновления данных
class ScheduleCDTO(BaseModel):
    zakaz: DTOConstant.StandardNullableVarcharField(description="Номер заказа")
    owner_id: DTOConstant.StandardNullableIntegerField(description="ID владельца")
    driver_id: DTOConstant.StandardNullableIntegerField(description="ID водителя")
    organization_id: DTOConstant.StandardNullableIntegerField(
        description="ID организации"
    )
    vehicle_id: DTOConstant.StandardNullableIntegerField(
        description="ID транспортного средства"
    )
    trailer_id: DTOConstant.StandardNullableIntegerField(description="ID прицепа")
    start_at: DTOConstant.StandardDateTimeField(description="Начало расписания")
    end_at: DTOConstant.StandardDateTimeField(description="Конец расписания")
    responsible_id: DTOConstant.StandardNullableIntegerField(
        description="ID ответственного лица"
    )

    class Config:
        from_attributes = True  # Привязка атрибутов модели SQLAlchemy


# DTO для чтения данных с расширенными связями
class ScheduleWithRelationsDTO(ScheduleRDTO):
    owner: Optional[UserRDTO] = None
    driver: Optional[UserRDTO] = None
    organization: Optional[OrganizationRDTO] = None
    vehicle: Optional[VehicleRDTO] = None
    trailer: Optional[VehicleRDTO] = None
    order: Optional[OrderRDTO] = None
    workshop_schedule: Optional[WorkshopScheduleRDTO] = None

    class Config:
        from_attributes = True  # Привязка атрибутов модели SQLAlchemy
