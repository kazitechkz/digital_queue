from typing import Optional

from pydantic import BaseModel

from app.adapters.dto.operation.operation_dto import OperationRDTO
from app.adapters.dto.schedule.schedule_dto import ScheduleRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant


class ScheduleHistoryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ScheduleHistoryCDTO(BaseModel):
    schedule_id: DTOConstant.StandardNullableIntegerField()
    operation_id: DTOConstant.StandardNullableIntegerField()
    responsible_id: DTOConstant.StandardNullableIntegerField()
    responsible_name: DTOConstant.StandardNullableVarcharField()
    responsible_iin: DTOConstant.StandardNullableVarcharField()
    is_passed: DTOConstant.StandardNullableBooleanField()
    start_at: DTOConstant.StandardNullableDateTimeField()
    end_at: DTOConstant.StandardNullableDateTimeField()
    canceled_at: DTOConstant.StandardNullableDateTimeField()
    cancel_reason: DTOConstant.StandardNullableTextField()

    class Config:
        from_attributes = True


class ScheduleHistoryRDTO(ScheduleHistoryDTO):
    schedule_id: DTOConstant.StandardNullableIntegerField()
    operation_id: DTOConstant.StandardNullableIntegerField()
    responsible_id: DTOConstant.StandardNullableIntegerField()
    responsible_name: DTOConstant.StandardNullableVarcharField()
    responsible_iin: DTOConstant.StandardNullableVarcharField()
    is_passed: DTOConstant.StandardNullableBooleanField()
    start_at: DTOConstant.StandardNullableDateTimeField()
    end_at: DTOConstant.StandardNullableDateTimeField()
    canceled_at: DTOConstant.StandardNullableDateTimeField()
    cancel_reason: DTOConstant.StandardNullableTextField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class ScheduleHistoryWithRelationsDTO(ScheduleHistoryDTO):
    schedule: Optional[ScheduleRDTO] = None
    operation: Optional[OperationRDTO] = None
    responsible: Optional[UserRDTO] = None
    canceled_by: Optional[UserRDTO] = None

    class Config:
        from_attributes = True
