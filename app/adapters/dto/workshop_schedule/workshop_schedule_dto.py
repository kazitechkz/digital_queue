from typing import Optional

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from app.adapters.dto.workshop.workshop_dto import WorkshopRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.shared.dto_constants import DTOConstant


class WorkshopScheduleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class WorkshopScheduleCDTO(BaseModel):
    workshop_id: DTOConstant.StandardIntegerField()
    workshop_sap_id: DTOConstant.StandardVarcharField()
    date_start: DTOConstant.StandardDateField()
    date_end: DTOConstant.StandardDateField()
    start_at: DTOConstant.StandardTimeField()
    end_at: DTOConstant.StandardTimeField()
    car_service_min: DTOConstant.StandardUnsignedIntegerField()
    break_between_service_min: DTOConstant.StandardUnsignedIntegerField()
    machine_at_one_time: DTOConstant.StandardUnsignedIntegerField()
    can_earlier_come_min: DTOConstant.StandardUnsignedIntegerField()
    can_late_come_min: DTOConstant.StandardUnsignedIntegerField()
    is_active: DTOConstant.StandardBooleanTrueField()

    @model_validator(mode="after")
    def check_dates_and_times(self) -> Self:
        date_start = self.date_start
        date_end = self.date_end
        start_at = self.start_at
        end_at = self.end_at

        # Проверка, что дата окончания больше даты начала
        if date_start and date_end and date_end <= date_start:
            msg = "Дата окончания должна быть больше даты начала"
            raise AppExceptionResponse.bad_request(message=msg)

        # Проверка, что время окончания больше времени начала
        if start_at and end_at and end_at <= start_at:
            msg = "Время окончания работы должна быть больше времени начала"
            raise AppExceptionResponse.bad_request(message=msg)

        return self

    class Config:
        from_attributes = True


class WorkshopScheduleRDTO(WorkshopScheduleDTO):
    workshop_id: DTOConstant.StandardNullableIntegerField()
    workshop_sap_id: DTOConstant.StandardVarcharField()
    date_start: DTOConstant.StandardDateField()
    date_end: DTOConstant.StandardDateField()
    start_at: DTOConstant.StandardTimeField()
    end_at: DTOConstant.StandardTimeField()
    car_service_min: DTOConstant.StandardIntegerField()
    break_between_service_min: DTOConstant.StandardIntegerField()
    machine_at_one_time: DTOConstant.StandardIntegerField()
    can_earlier_come_min: DTOConstant.StandardIntegerField()
    can_late_come_min: DTOConstant.StandardIntegerField()
    is_active: DTOConstant.StandardBooleanTrueField()

    class Config:
        from_attributes = True


class WorkshopScheduleWithRelationsDTO(WorkshopScheduleRDTO):
    workshop: Optional[WorkshopRDTO] = None

    class Config:
        from_attributes = True
