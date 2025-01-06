from typing import Optional

from pydantic import BaseModel, Field


class AdditionalAttributesDTO(BaseModel):
    iin: Optional[str] = Field(None, description="ИИН пользователя")
    position: Optional[str] = Field(None, description="Должность пользователя")


class UserResponseDTO(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    mobile: Optional[str] = Field(None)
    additional_attributes: AdditionalAttributesDTO

    class Config:
        populate_by_name = True
