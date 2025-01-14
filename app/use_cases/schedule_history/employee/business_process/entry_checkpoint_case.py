from typing import Optional, List

from app.adapters.dto.schedule_history.make_decision_dto import MakeDecisionDTO
from app.adapters.dto.schedule_history.schedule_history_dto import ScheduleHistoryWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.schedule.schedule_repository import ScheduleRepository
from app.adapters.repositories.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.entities import ScheduleModel, ScheduleHistoryModel, OperationModel
from app.use_cases.base_case import BaseUseCase
from sqlalchemy.ext.asyncio import AsyncSession


class EntryCheckPointCase(BaseUseCase[ScheduleHistoryWithRelationsDTO]):

    def __init__(self,
                 db: AsyncSession
                 ):
        self.schedule_history_repository = ScheduleHistoryRepository(db)
        self.schedule_repository = ScheduleRepository(db)
        self.dto:Optional[MakeDecisionDTO] = None
        self.schedule:Optional[ScheduleModel] = None
        self.employee:Optional[UserWithRelationsDTO] = None
        self.operations:List[OperationModel] = None

    async def execute(
            self,
            dto:MakeDecisionDTO,
            schedule:ScheduleModel,
            employee:UserWithRelationsDTO,
            operations:List[OperationModel]
            ) -> ScheduleHistoryModel:
        self.schedule = schedule
        self.employee = employee
        self.dto = dto
        self.operations = operations

    async def validate(self):
        pass

    async def transform(self):
        pass





