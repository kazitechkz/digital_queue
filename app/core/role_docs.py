from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from starlette.templating import Jinja2Templates

from app.infrastructure.config import AppConfiguration, app_config
from app.shared.app_route_constant import AppRouteConstant


def custom_openapi(app, role: str, role_name: str):
    routes = [
        route for route in app.routes if hasattr(route, "roles") and role in route.roles
    ]
    openapi_schema = get_openapi(
        title=f"{app_config.app_name}({role_name})",
        description=app_config.app_description,
        version=app_config.app_version,
        routes=routes,
    )
    return openapi_schema


def setup_role_documentation(app) -> None:
    admin_docs_url = f"{app_config.app_docs_url}{app_config.app_administrator_docs_url}"
    employee_docs_url = f"{app_config.app_docs_url}{app_config.app_employee_docs_url}"
    client_docs_url = f"{app_config.app_docs_url}{app_config.app_client_docs_url}"
    # Указываем папку с шаблонами
    templates = Jinja2Templates(directory="templates")

    @app.get(f"{app_config.app_starter_page_url}", include_in_schema=False)
    async def get_roles_page(request: Request):
        return templates.TemplateResponse(
            "start_page.html.jinja",
            {
                "request": request,
                "admin_docs_url": admin_docs_url,
                "employee_docs_url": employee_docs_url,
                "client_docs_url": client_docs_url,
            },
        )

    @app.get(admin_docs_url, include_in_schema=False)
    async def get_admin_docs():
        return get_swagger_ui_html(
            openapi_url=f"/openapi/{admin_docs_url}",
            title=AppRouteConstant.AdministratorName,
        )

    @app.get(client_docs_url, include_in_schema=False)
    async def get_user_docs():
        return get_swagger_ui_html(
            openapi_url=f"/openapi/{client_docs_url}", title=AppRouteConstant.ClientName
        )

    @app.get(employee_docs_url, include_in_schema=False)
    async def get_employee_docs():
        return get_swagger_ui_html(
            openapi_url=f"/openapi/{employee_docs_url}",
            title=AppRouteConstant.EmployeesName,
        )

    # OpenAPI схемы для каждой роли
    @app.get(f"/openapi/{admin_docs_url}", include_in_schema=False)
    async def get_admin_openapi():
        return custom_openapi(
            app,
            AppRouteConstant.AdministratorTagName,
            AppRouteConstant.AdministratorName,
        )

    @app.get(f"/openapi/{client_docs_url}", include_in_schema=False)
    async def get_user_openapi():
        return custom_openapi(
            app, AppRouteConstant.ClientTagName, AppRouteConstant.ClientName
        )

    @app.get(f"/openapi/{employee_docs_url}", include_in_schema=False)
    async def get_employee_openapi():
        return custom_openapi(
            app, AppRouteConstant.EmployeesTagName, AppRouteConstant.EmployeesName
        )
