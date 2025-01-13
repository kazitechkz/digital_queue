from typing import List

from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class CreateLegalSapOrderDTO(BaseModel):
    DOGOVOR: DTOConstant.SAP_DOGOVOR_FIELD()
    MATNR: DTOConstant.MATNR_FIELD()
    QUAN: DTOConstant.SAP_QUAN_FIELD()
    ORDER_ID: DTOConstant.SAP_ORDER_ID_FIELD()

    class Config:
        from_attributes = True


class CreateIndividualSapOrderDTO(BaseModel):
    WERKS: DTOConstant.WERKS_FIELD()
    MATNR: DTOConstant.MATNR_FIELD()
    KUN_NAME: DTOConstant.KUN_NAME_FIELD()
    ADR_INDEX: DTOConstant.SAP_ADR_INDEX_FIELD()
    ADR_CITY: DTOConstant.SAP_ADR_CITY_FIELD()
    ADR_STR: DTOConstant.SAP_ADR_STR_FIELD()
    ADR_DOM: DTOConstant.SAP_ADR_DOM_FIELD()
    IIN: DTOConstant.StandardUniqueIINField()
    QUAN: DTOConstant.SAP_QUAN_FIELD()
    PRICE: DTOConstant.StandardPriceField()
    ORDER_ID: DTOConstant.SAP_ORDER_ID_FIELD()

    class Config:
        from_attributes = True


class SapOrderStatusItemDTO(BaseModel):
    STATUS: DTOConstant.StandardNullableIntegerField() = None
    ZAKAZ: DTOConstant.StandardNullableVarcharField() = None
    PDF: DTOConstant.SAP_PDF() = None
    TEXT: DTOConstant.SAP_TEXT() = None
    DATE: DTOConstant.SAP_DATE() = None
    TIME: DTOConstant.SAP_TIME() = None
    ORDER_ID: DTOConstant.SAP_NULLABLE_ORDER_ID_FIELD() = None

    class Config:
        from_attributes = True


class SapStatusDTO(BaseModel):
    items: List[SapOrderStatusItemDTO]
