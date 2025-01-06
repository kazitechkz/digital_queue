from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.app_cors import set_up_cors
from infrastructure.config import app_config
from starlette.staticfiles import StaticFiles

from app.core.api_routes import include_routers
from app.core.app_exception_handler import validation_exception_handler
from app.core.auth_bearer_core import AuthBearer
from app.core.role_docs import setup_role_documentation
from app.core.role_routes import assign_roles
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
    dependencies=[Depends(AuthBearer())],
)


# Включаем все роутеры
include_routers(app)

app.mount(
    f"/{app_config.static_folder}",
    StaticFiles(directory=f"{app_config.static_folder}"),
    name=f"{app_config.static_folder}",
)

# Включаем роутизацию для ролей
setup_role_documentation(app)
assign_roles(app)
# Регистрация обработчика
app.add_exception_handler(RequestValidationError, validation_exception_handler)
#Middleware
set_up_cors(app)


# Запуск сервера
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
