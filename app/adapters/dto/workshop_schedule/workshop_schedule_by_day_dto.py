from datetime import date

from pydantic import BaseModel

from app.shared.query_constants import AppQueryConstants


class WorkshopScheduleByDayDTO(BaseModel):
    workshop_sap_id: str = AppQueryConstants.StandardOptionalStringQuery(
        description="SAP ID цеха"
    )
    schedule_date: date = AppQueryConstants.StandardOptionalDateForScheduleQuery(
        description="День записи"
    )

    class Config:
        from_attributes = True
