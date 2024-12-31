from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from infrastructure.config import app_config
from starlette.staticfiles import StaticFiles

from app.core.api_routes import include_routers
from app.core.app_exception_handler import validation_exception_handler
from app.seeders.runner import run_seeders


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_seeders()
    yield


app = FastAPI(
    title=app_config.app_name,
    description=app_config.app_description,
    version=app_config.app_version,
    lifespan=lifespan,
    debug=True,
    docs_url=app_config.app_docs_url,
    redoc_url=None,
)


# Включаем все роутеры
include_routers(app)

app.mount(
    f"/{app_config.static_folder}",
    StaticFiles(directory=f"{app_config.static_folder}"),
    name=f"{app_config.static_folder}",
)

# Регистрация обработчика
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Запуск сервера
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
