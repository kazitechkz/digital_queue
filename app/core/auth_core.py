from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Dict, List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.entities import UserModel
from app.infrastructure.config import app_config
from app.infrastructure.database import get_db
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.auth.get_current_user_case import GetCurrentUserCase

# Утилиты и конфигурации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Хэширование и проверка паролей ===
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# === Работа с токенами ===
def create_access_token(data: int) -> str:
    """Создает Access Token."""
    to_encode = {"sub": str(data), "type": "access"}
    expire = datetime.now() + timedelta(minutes=app_config.access_token_expire_minutes)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, app_config.secret_key, algorithm=app_config.algorithm)


def create_refresh_token(data: int) -> str:
    """Создает Refresh Token."""
    to_encode = {"sub": str(data), "type": "refresh"}
    expire = datetime.now() + timedelta(days=app_config.refresh_token_expire_days)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, app_config.secret_key, algorithm=app_config.algorithm)

# === Получение текущего пользователя ===
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> UserWithRelationsDTO:
    use_case = GetCurrentUserCase(db)
    return await use_case.execute(token)




