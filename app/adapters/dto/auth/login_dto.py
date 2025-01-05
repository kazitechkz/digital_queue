from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class LoginDTO(BaseModel):
    username: DTOConstant.StandardTextField()
    password: DTOConstant.StandardTextField()