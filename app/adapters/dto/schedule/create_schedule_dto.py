from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class CreateScheduleDTO(BaseModel):
    order_id: DTOConstant.StandardIntegerField(description="Идентификатор заказа")
    workshop_schedule_id: DTOConstant.StandardIntegerField(
        description="Идентификатор расписания цеха"
    )
    scheduled_data: DTOConstant.StandardDateField(description="Дата записи")
    start_at: DTOConstant.StandardTimeField(description="Время начала записи")
    end_at: DTOConstant.StandardTimeField(description="Время окончания записи")
    vehicle_id: DTOConstant.StandardIntegerField(
        description="Идентификатор транспортного средства"
    )
    trailer_id: DTOConstant.StandardNullableIntegerField(
        description="Идентификатор прицепа"
    )
    booked_quan_t: DTOConstant.StandardPriceField(
        description="Забронированный объем в тоннах"
    )
    # Поля для юридических лиц
    organization_id: DTOConstant.StandardNullableIntegerField(
        description="Идентификатор организации (только для юр. лиц)"
    )
    driver_id: DTOConstant.StandardNullableIntegerField(
        description="Идентификатор водителя (только для юр. лиц)"
    )
