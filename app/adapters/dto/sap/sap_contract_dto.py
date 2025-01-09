from typing import Optional, List

from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant

class SapContractRowItemDTO(BaseModel):
    POSNR: DTOConstant.StandardNullableVarcharField(description="Номер позиции")
    MATNR: DTOConstant.StandardNullableVarcharField(description="Номер материала")
    ARKTX: DTOConstant.StandardNullableVarcharField(description="Наименование материала")
    ZWERT: DTOConstant.StandardNullableVarcharField(description="Сумма договора")
    ZWERT_RST: DTOConstant.StandardNullableVarcharField(description="Договорная стоимость остатка")
    WAERK: DTOConstant.StandardNullableVarcharField(description="Валюта заключенная договором")
    ZMENG: DTOConstant.StandardNullableVarcharField(description="Колличество по договору")
    ZMENG_RST: DTOConstant.StandardNullableVarcharField(description="Оставшийся остаток")
    ZIEME: DTOConstant.StandardNullableVarcharField(description="Единициа измерения объема")
    STATUS: DTOConstant.StandardNullableVarcharField(description="Завершен или не завершен")
class SapContractRowDTO(BaseModel):
    KTEXT: DTOConstant.StandardNullableVarcharField(description="Юридический номер договора")
    VTEXT: DTOConstant.StandardNullableVarcharField(description="Сбыт организация")
    ZNAME: DTOConstant.StandardNullableVarcharField(description="Куратор заявки")
    MSG: DTOConstant.StandardNullableVarcharField(description="Сообщение заявки OK и если нет Not found")
    item: Optional[List[SapContractRowItemDTO]]

class SapContractDTO(BaseModel):
    row: Optional[List[SapContractRowDTO]]

class SapContractForResponseDTO(BaseModel):
    dogovor:DTOConstant.StandardNullableVarcharField(description="Юридический номер договора")
    material_sap_id:DTOConstant.StandardNullableVarcharField(description="Номер материала")
    total_price: DTOConstant.StandardNullablePriceField(description="Сумма договора")
    rest_price: DTOConstant.StandardNullablePriceField(description="Договорная стоимость остатка")
    quan_t:DTOConstant.StandardNullablePriceField(description="Колличество по договору")
    quan_t_left:DTOConstant.StandardNullablePriceField(description="Оставшийся остаток")