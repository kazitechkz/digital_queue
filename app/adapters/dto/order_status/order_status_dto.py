from typing import Optional

from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class OrderStatusDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class OrderStatusCDTO(BaseModel):
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    prev_id: DTOConstant.StandardNullableIntegerField()
    next_id: DTOConstant.StandardNullableIntegerField()
    prev_value: DTOConstant.StandardNullableVarcharField()
    next_value: DTOConstant.StandardNullableVarcharField()
    is_first: DTOConstant.StandardNullableBooleanField()
    is_last: DTOConstant.StandardNullableBooleanField()

    class Config:
        from_attributes = True


class OrderStatusRDTO(OrderStatusDTO):
    id: DTOConstant.StandardID()
    title: DTOConstant.StandardTitleField()
    value: DTOConstant.StandardUniqueValueField()
    prev_id: DTOConstant.StandardNullableIntegerField()
    next_id: DTOConstant.StandardNullableIntegerField()
    prev_value: DTOConstant.StandardNullableVarcharField()
    next_value: DTOConstant.StandardNullableVarcharField()
    is_first: DTOConstant.StandardNullableBooleanField()
    is_last: DTOConstant.StandardNullableBooleanField()
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class OrderStatusWithRelationsDTO(OrderStatusRDTO):
    prev_order_status: Optional[OrderStatusRDTO]
    next_order_status: Optional[OrderStatusRDTO]

    class Config:
        from_attributes = True
