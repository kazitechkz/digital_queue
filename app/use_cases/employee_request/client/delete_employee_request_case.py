from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.employee_request.employee_request_repository import EmployeeRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class DeleteEmployeeRequestCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = EmployeeRequestRepository(db)

    async def execute(self, id: int,user:UserWithRelationsDTO) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int,user:UserWithRelationsDTO):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Заявка не найдена")
        if existed.owner_id != user.id:
            raise AppExceptionResponse.not_found(message="Вы не можете удалить заявку")

