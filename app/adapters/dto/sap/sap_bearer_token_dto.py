from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class SapBearerTokenDTO(BaseModel):
    access_token:DTOConstant.StandardVarcharField()
    token_type:DTOConstant.StandardVarcharField()
    expires_in:DTOConstant.StandardIntegerField()