from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class WorkshopScheduleSpaceDTO(BaseModel):
    workshop_schedule_id: DTOConstant.StandardIntegerField(
        description="Идентификатор Цеха"
    )
    scheduled_data: DTOConstant.StandardDateField(description="День бронирования")
    start_at: DTOConstant.StandardTimeField(description="Начало бронирования")
    end_at: DTOConstant.StandardTimeField(description="Конец бронирования")
    free_space: DTOConstant.StandardIntegerField(description="Идентификатор Цеха")
