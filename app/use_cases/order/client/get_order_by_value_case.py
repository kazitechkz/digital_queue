from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.order.order_repository import OrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetClientOrderByValueCase(BaseUseCase[OrderWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def execute(
        self, value: str, user: UserWithRelationsDTO
    ) -> OrderWithRelationsDTO:
        filters = [
            and_(
                or_(
                    func.lower(self.repository.model.status) == value.lower(),
                    func.lower(self.repository.model.factory_sap_id) == value.lower(),
                    func.lower(self.repository.model.workshop_sap_id) == value.lower(),
                    func.lower(self.repository.model.material_sap_id) == value.lower(),
                    func.lower(self.repository.model.zakaz) == value.lower(),
                    func.lower(self.repository.model.txn_id) == value.lower(),
                    func.lower(self.repository.model.iin) == value.lower(),
                    func.lower(self.repository.model.owner_sid) == value.lower(),
                    func.lower(self.repository.model.owner_username) == value.lower(),
                    func.lower(self.repository.model.owner_email) == value.lower(),
                    func.lower(self.repository.model.owner_mobile) == value.lower(),
                    func.lower(self.repository.model.name) == value.lower(),
                    func.lower(self.repository.model.adr_index) == value.lower(),
                    func.lower(self.repository.model.adr_city) == value.lower(),
                    func.lower(self.repository.model.adr_str) == value.lower(),
                    func.lower(self.repository.model.adr_dom) == value.lower(),
                    func.lower(self.repository.model.bin) == value.lower(),
                    func.lower(self.repository.model.dogovor) == value.lower(),
                    func.lower(self.repository.model.canceled_by_sid) == value.lower(),
                    func.lower(self.repository.model.checked_payment_by)
                    == value.lower(),
                ),
                or_(
                    self.repository.model.owner_id == user.id,
                    self.repository.model.iin == user.iin,
                    self.repository.model.owner_sid == user.sid,
                ),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Заказ не найден")
        return OrderWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
