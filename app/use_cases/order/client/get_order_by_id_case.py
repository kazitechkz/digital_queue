from sqlalchemy import or_,and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.order.order_repository import OrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetClientOrderByIdCase(BaseUseCase[OrderWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def execute(self, id: int,user:UserWithRelationsDTO) -> OrderWithRelationsDTO:
        model = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    or_(
                        self.repository.model.owner_id == user.id,
                        self.repository.model.iin == user.iin,
                        self.repository.model.owner_sid == user.sid,
                    )
                )
            ],
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Заказ не найден")
        return OrderWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
