from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class CreateOrderDTO(BaseModel):
    material_sap_id: DTOConstant.StandardVarcharField(description="Материал SAP ID")
    quan_t: DTOConstant.StandardPriceField(description="Объем в тоннах")
    dogovor: DTOConstant.StandardNullableVarcharField(
        description="Договор юр лица получаемая из SAP"
    )
    organization_id: DTOConstant.StandardNullableIntegerField(
        description="Идентификатор компании"
    )
    adr_index: DTOConstant.StandardVarcharField(description="Индекс почтовый")
    adr_city: DTOConstant.StandardVarcharField(description="Город")
    adr_str: DTOConstant.StandardVarcharField(description="Улица")
    adr_dom: DTOConstant.StandardVarcharField(description="Дом, квартира")

    class Config:
        from_attributes = True
