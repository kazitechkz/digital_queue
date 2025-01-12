import aiohttp
from aiohttp import ClientResponseError
from fastapi import HTTPException
from starlette import status

from app.adapters.dto.user.user_response_dto import UserResponseDTO
from app.infrastructure.config import app_config


class UserRepoApiClient:
    def __init__(self, token: str, base_url: str = None):
        self.base_url = base_url or app_config.get_user_repo_url()
        self.token = token

    async def get_current_user(self):
        url = f"{self.base_url}/user-repository/current-user"
        headers = {"Authorization": f"Bearer {self.token}"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        raw_data = await response.json()
                        user = UserResponseDTO.parse_obj(raw_data)
                        return user
                    elif response.status == 401:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Не авторизован: проверьте токен",
                        )
                    elif response.status == 403:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Доступ запрещен",
                        )
                    else:
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Ошибка запроса: {await response.text()}",
                        )
            except aiohttp.ClientResponseError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Ошибка внешнего API {url}: {e.status} {e.message}",
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Непредвиденная ошибка: {str(e)}",
                )

    def generate_fake_mobile_iin(self) -> dict:
        return {"iin": "123123123123", "mobile": ""}
