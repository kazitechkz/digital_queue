from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class BearerTokenDTO(BaseModel):
    access_token: DTOConstant.StandardTextField()
    refresh_token: DTOConstant.StandardNullableTextField()

    class Config:
        from_attributes = True
