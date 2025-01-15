from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderCDTO
from app.adapters.dto.schedule.create_schedule_dto import CreateScheduleDTO
from app.adapters.dto.schedule.schedule_dto import ScheduleWithRelationsDTO, ScheduleRDTO, ScheduleCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.dto.workshop_schedule.workshop_schedule_by_day_dto import WorkshopScheduleByDayDTO
from app.adapters.dto.workshop_schedule.workshop_schedule_space_dto import WorkshopScheduleSpaceDTO
from app.adapters.repositories.operation.operation_repository import OperationRepository
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.order_status.order_status_repository import OrderStatusRepository
from app.adapters.repositories.organization.organization_repository import OrganizationRepository
from app.adapters.repositories.organization_employee.organization_employee_repository import \
    OrganizationEmployeeRepository
from app.adapters.repositories.schedule.schedule_repository import ScheduleRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import WorkshopScheduleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OrderModel, OrganizationModel, VehicleModel, ScheduleModel, OperationModel
from app.infrastructure.config import app_config
from app.infrastructure.helpers.vehicle_helper import VehicleHelper
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase
from app.use_cases.order.recalculate_order_by_id_case import RecalculateOrderByIdCase
from app.use_cases.workshop_schedule.get_workshop_schedule_by_day_case import GetWorkshopScheduleByDayCase


class CreateClientScheduleCase(BaseUseCase[ScheduleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = ScheduleRepository(db)
        self.user_repository = UserRepository(db)
        self.vehicle_repository = VehicleRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.organization_employee_repository = OrganizationEmployeeRepository(db)
        self.get_workshop_schedule_by_day_case = GetWorkshopScheduleByDayCase(db)
        self.recalculate_order_by_id_case = RecalculateOrderByIdCase(db)
        self.order_repository = OrderRepository(db)
        self.order_status_repository = OrderStatusRepository(db)
        self.operation_repository = OperationRepository(db)
        self.workshop_schedule_repository = WorkshopScheduleRepository(db)
        #Global Variables
        self.order:Optional[OrderModel] = None
        self.driver = None
        self.organization:Optional[OrganizationModel] = None
        self.vehicle:Optional[VehicleModel] = None
        self.trailer:Optional[VehicleModel] = None
        self.operation:Optional[OperationModel] = None


    async def execute(
        self,
        user: UserWithRelationsDTO,
        dto: CreateScheduleDTO,
    ):
        await self.validate(dto=dto, user=user)
        operation = await self.operation_repository.first_operation()
        if not operation:
            raise AppExceptionResponse.bad_request(message="Первичная операция не найдена")
        self.operation = operation
        cdto = await self.transform(dto=dto,user=user)
        model = await self.repository.create(obj=ScheduleModel(**cdto.dict()))
        if not model:
            raise AppExceptionResponse.internal_error(message="Произошла ошибка при создании расписания")
        await self._update_order()
        await self.recalculate_order_by_id_case.execute(id=self.order.id)
        model = await self.repository.get(id=model.id,options=self.repository.default_relationships())
        return ScheduleWithRelationsDTO.from_orm(model)


    async def transform(self, dto: CreateScheduleDTO, user: UserWithRelationsDTO)->ScheduleCDTO:
       return ScheduleCDTO(
            order_id = dto.order_id,
            zakaz = self.order.zakaz if self.order else None,
            owner_id = user.id,
            owner_name = user.name,
            owner_iin = user.iin,
            owner_sid = user.sid,
            driver_id = self.driver.id if self.driver else None,
            driver_name = self.driver.name if self.driver else None,
            driver_iin = self.driver.iin if self.driver else None,
            driver_sid = self.driver.sid if self.driver else None,
            organization_id = self.organization.id if self.organization else None,
            organization_full_name = self.organization.full_name if self.organization else None,
            organization_bin = self.organization.bin if self.organization else None,
            vehicle_id=self.vehicle.id if self.vehicle else None,
            vehicle_info = self.vehicle.vehicle_info if self.vehicle else None,
            trailer_id = self.trailer.id if self.trailer else None,
            trailer_info = self.trailer.vehicle_info if self.trailer else None,
            car_number = VehicleHelper.get_vehicle_registration_number(self.vehicle,self.trailer),
            workshop_schedule_id = dto.workshop_schedule_id,
            current_operation_id=self.operation.id,
            current_operation_name=self.operation.title,
            current_operation_value=self.operation.value,
            start_at=datetime.combine(dto.scheduled_data, dto.start_at),
            end_at=datetime.combine(dto.scheduled_data, dto.end_at),
            rescheduled_start_at=None,
            rescheduled_end_at=None,
            loading_volume=dto.booked_quan_t,
            vehicle_tara = 0,
            vehicle_netto = 0,
            vehicle_brutto = 0,
            responsible_id = None,
            responsible_name = None,
            is_active = True,
            is_used = False,
            is_canceled = False,
            is_executed = False,
            executed_at = None,
            canceled_by = None,
            canceled_by_name = None,
            canceled_by_sid = None,
            cancel_reason = None,
            canceled_at = None
       )



    async def validate(self, dto: CreateScheduleDTO, user: UserWithRelationsDTO):
        # Проверяем доступ к заказу
        order = await self._validate_order_access(dto, user)

        # Проверяем расписание
        workshop_schedule = await self._validate_schedule(dto)

        # Проверяем доступное время
        await self._validate_available_times(dto, workshop_schedule)

        # Проверяем организацию (для юр. лиц)
        if user.user_type.value == AppDbValueConstants.LEGAL_VALUE:
            await self._validate_organization_access(dto, user)

        # Проверяем водителя
        await self._validate_driver_access(dto, user)

        # Проверяем транспортное средство
        await self._validate_vehicle_access(dto, user)


    async def _update_order(self):
        if self.order:
            if self.order.status == AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS:
                order_dto = OrderCDTO.from_orm(self.order)
                next_order = await self.order_status_repository.get_first_with_filters(
                    filters=[
                        and_(
                            func.lower(self.order_status_repository.model.value) == AppDbValueConstants.IN_PROGRESS_STATUS
                        )
                    ],
                )
                order_dto.status = next_order.value
                order_dto.status_id = next_order.id
                self.order = await self.order_repository.update(obj=self.order,dto=order_dto)


    async def _validate_order_access(self, dto: CreateScheduleDTO, user: UserWithRelationsDTO):
        available_order_statuses = await self.order_status_repository.get_with_filters(
            filters=[
                and_(
                    self.order_status_repository.model.value.in_(
                        [AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS, AppDbValueConstants.IN_PROGRESS_STATUS]
                    ),
                    self.order_status_repository.model.status == True
                )
            ],
        )
        available_order_statuses_ids = [order_status.id for order_status in available_order_statuses]
        organization_ids = [organization.id for organization in user.organizations if organization.is_verified]

        order = await self.order_repository.get_first_with_filters(
            filters=[
                and_(
                    self.order_repository.model.status_id.in_(available_order_statuses_ids),
                    or_(
                        self.order_repository.model.owner_id == user.id,
                        self.order_repository.model.organization_id.in_(organization_ids)
                    ),
                    self.order_repository.model.is_paid == True
                )
            ],
            options=self.order_repository.default_relationships()
        )
        if not order:
            raise AppExceptionResponse.bad_request(message="Заказ не найден")
        self.order = order

    async def _validate_schedule(self, dto: CreateScheduleDTO):
        workshop_schedule = await self.workshop_schedule_repository.get_first_with_filters(
            filters=[
                self.workshop_schedule_repository.model.id == dto.workshop_schedule_id,
            ]
        )
        if not workshop_schedule:
            raise AppExceptionResponse.bad_request(message="Расписание не найдено")
        return workshop_schedule

    async def _validate_available_times(self, dto: CreateScheduleDTO, workshop_schedule):
        get_free_space_dto = WorkshopScheduleByDayDTO(
            workshop_sap_id=workshop_schedule.workshop_sap_id,
            schedule_date=dto.scheduled_data
        )
        available_times: List[WorkshopScheduleSpaceDTO] = await self.get_workshop_schedule_by_day_case.execute(
            dto=get_free_space_dto)
        if not available_times:
            raise AppExceptionResponse.bad_request(message="В выбранную дату нет свободного времени")
        for available_time in available_times:
            if available_time.start_at == dto.start_at or available_time.end_at == dto.end_at or available_time.free_space > 0:
                return True
        raise AppExceptionResponse.bad_request(message="Недостаточно места в выбранное время")

    async def _validate_organization_access(self):
        if not self.order.organization:
            raise AppExceptionResponse.bad_request("Не указана организация")
        self.organization = self.order.organization

    async def _validate_driver_access(self, dto: CreateScheduleDTO, user: UserWithRelationsDTO):
        if not dto.driver_id:
            raise AppExceptionResponse.bad_request(message="Не указан водитель")
        if user.user_type.value == AppDbValueConstants.LEGAL_VALUE and dto.driver_id != user.id:
            organization_employee = await self.organization_employee_repository.get_first_with_filters(
                filters=[
                    and_(
                        self.organization_employee_repository.model.employee_id == dto.driver_id,
                        self.organization_employee_repository.model.organization_id == dto.organization_id,
                    )
                ]
            )
            if not organization_employee:
                raise AppExceptionResponse.bad_request(message="У вас нет доступа к этому водителю")
        elif user.user_type.value == AppDbValueConstants.INDIVIDUAL_VALUE and dto.driver_id != user.id:
            raise AppExceptionResponse.bad_request(message="У вас нет доступа к этому водителю")

        if dto.driver_id != user.id:
            self.driver = await self.user_repository.get(dto.driver_id)
        else:
            self.driver = user


    async def _validate_vehicle_access(self, dto: CreateScheduleDTO, user: UserWithRelationsDTO):
        organization_ids = [organization.id for organization in user.organizations if organization.is_verified]
        if dto.trailer_id:
            trailer = await self.vehicle_repository.get_first_with_filters(
                filters=[
                    and_(
                        self.vehicle_repository.model.id == dto.trailer_id,
                        or_(
                            self.vehicle_repository.model.owner_id == user.id,
                            self.vehicle_repository.model.organization_id.in_(organization_ids)
                        ),
                    )
                ]
            )
            if not trailer:
                raise AppExceptionResponse.bad_request(message="У вас нет доступа к этому прицепу")
            self.trailer = trailer
        vehicle = await self.vehicle_repository.get_first_with_filters(
            filters=[
                and_(
                    self.vehicle_repository.model.id == dto.vehicle_id,
                    or_(
                        self.vehicle_repository.model.owner_id == user.id,
                        self.vehicle_repository.model.organization_id.in_(organization_ids)
                    ),
                )
            ]
        )
        if not vehicle:
            raise AppExceptionResponse.bad_request(message="У вас нет доступа к этому ТС")
        if dto.booked_quan_t >= app_config.max_booked_quan_t or dto.booked_quan_t <= app_config.min_booked_quan_t:
            raise AppExceptionResponse.bad_request(message=f"Количество забронированных количество вне допустимого диапазона {app_config.min_booked_quan_t} - {app_config.max_booked_quan_t} тонн")

        if dto.booked_quan_t > self.order.quan_left_t:
            raise AppExceptionResponse.bad_request(message=f"У вас недостаточно материала для данного заказа {dto.booked_quan_t - self.order.quan_left_t} превышено!")
        self.vehicle = vehicle