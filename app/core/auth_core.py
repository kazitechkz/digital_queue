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
    return jwt.encode(to_encode, app_config.SECRET_KEY, algorithm=app_config.algorithm)


def create_refresh_token(data: int) -> str:
    """Создает Refresh Token."""
    to_encode = {"sub": str(data), "type": "refresh"}
    expire = datetime.now() + timedelta(days=app_config.refresh_token_expire_days)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, app_config.SECRET_KEY, algorithm=app_config.algorithm)


def decode_jwt(token: str, token_type: str) -> Dict:
    """Декодирует JWT-токен и проверяет его тип."""
    try:
        decoded_data = jwt.decode(
            token, app_config.SECRET_KEY, algorithms=[app_config.algorithm]
        )
        if decoded_data.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недопустимый токен для {token_type} операций",
            )
        return decoded_data
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Ошибка проверки токена: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# === Декодирование токенов ===
def verify_access_token(token: str = Depends(oauth2_scheme)) -> Dict:
    """Проверяет Access Token."""
    return decode_jwt(token, "access")


def verify_refresh_token(token: str = Depends(oauth2_scheme)) -> Dict:
    """Проверяет Refresh Token."""
    return decode_jwt(token, "refresh")


# === Получение текущего пользователя ===
async def get_current_user(
    token: Dict = Depends(verify_access_token), db: AsyncSession = Depends(get_db)
) -> UserWithRelationsDTO:
    """Получает текущего пользователя по токену."""
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Идентификатор пользователя отсутствует в токене",
        )

    query = (
        select(UserModel)
        .options(
            selectinload(UserModel.role),
            selectinload(UserModel.user_type),
            selectinload(UserModel.organizations),
        )
        .filter(UserModel.id == int(user_id))
    )
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return UserWithRelationsDTO.from_orm(user)


# === Универсальные проверки ролей и типов ===
def check_roles(
    current_user: UserWithRelationsDTO, roles: List[str]
) -> UserWithRelationsDTO:
    """Проверяет, принадлежит ли пользователь к указанным ролям."""
    if current_user.role.value not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа",
        )
    return current_user


def check_user_type(
    current_user: UserWithRelationsDTO, user_type: str
) -> UserWithRelationsDTO:
    """Проверяет тип пользователя."""
    if current_user.user_type.value != user_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа",
        )
    return current_user


# === Специфические проверки ===
def check_admin(current_user: UserWithRelationsDTO = Depends(get_current_user)):
    return check_roles(current_user, [AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE])


def check_security(current_user: UserWithRelationsDTO = Depends(get_current_user)):
    return check_roles(current_user, [AppDbValueConstants.SECURITY_KEYCLOAK_VALUE])


def check_client(current_user: UserWithRelationsDTO = Depends(get_current_user)):
    return check_roles(current_user, [AppDbValueConstants.RoleClientValue])


def check_individual_client(
    current_user: UserWithRelationsDTO = Depends(get_current_user),
):
    check_roles(current_user, [AppDbValueConstants.RoleClientValue])
    return check_user_type(current_user, AppDbValueConstants.UserIndividualTypeValue)


def check_legal_client(current_user: UserWithRelationsDTO = Depends(get_current_user)):
    check_roles(current_user, [AppDbValueConstants.RoleClientValue])
    return check_user_type(current_user, AppDbValueConstants.UserLegalTypeValue)


# Пример объединенной проверки
def check_admin_and_employee(
    current_user: UserWithRelationsDTO = Depends(get_current_user),
):
    return check_roles(
        current_user,
        [
            AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
            AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
            AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
            AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
        ],
    )
