from app.adapters.api.factory.factory_api import FactoryApi
from app.adapters.api.file.file_api import FileApi
from app.adapters.api.material.material_api import MaterialApi
from app.adapters.api.operation.operation_api import OperationApi
from app.adapters.api.order_status.order_status_api import OrderStatusApi
from app.adapters.api.organization_type.organization_type_api import OrganizationTypeApi
from app.adapters.api.role.role_api import RoleApi
from app.adapters.api.test.test_api import TestApi
from app.adapters.api.user.user_api import UserApi
from app.adapters.api.user_type.user_type_api import UserTypeApi
from app.adapters.api.vehicle_category.vehicle_category_api import VehicleCategoryApi
from app.adapters.api.vehicle_color.vehicle_color_api import VehicleColorApi
from app.adapters.api.workshop.workshop_api import WorkshopApi
from app.adapters.api.workshop_schedule.workshop_schedule_api import WorkshopScheduleApi
from app.shared.path_constants import AppPathConstants


def include_routers(app) -> None:
    app.include_router(
        RoleApi().router,
        prefix=f"/{AppPathConstants.RolePathName}",
        tags=[AppPathConstants.RoleTagName],
    )
    app.include_router(
        UserTypeApi().router,
        prefix=f"/{AppPathConstants.UserTypePathName}",
        tags=[AppPathConstants.UserTypeTagName],
    )
    app.include_router(
        FileApi().router,
        prefix=f"/{AppPathConstants.FilePathName}",
        tags=[AppPathConstants.FileTagName],
    )
    app.include_router(
        OrganizationTypeApi().router,
        prefix=f"/{AppPathConstants.OrganizationTypePathName}",
        tags=[AppPathConstants.OrganizationTypeTagName],
    )
    app.include_router(
        VehicleColorApi().router,
        prefix=f"/{AppPathConstants.VehicleColorPathName}",
        tags=[AppPathConstants.VehicleColorTagName],
    )
    app.include_router(
        VehicleCategoryApi().router,
        prefix=f"/{AppPathConstants.VehicleCategoryPathName}",
        tags=[AppPathConstants.VehicleCategoryTagName],
    )
    app.include_router(
        OrderStatusApi().router,
        prefix=f"/{AppPathConstants.OrderStatusPathName}",
        tags=[AppPathConstants.OrderStatusTagName],
    )
    app.include_router(
        OperationApi().router,
        prefix=f"/{AppPathConstants.OperationPathName}",
        tags=[AppPathConstants.OperationTagName],
    )
    app.include_router(
        FactoryApi().router,
        prefix=f"/{AppPathConstants.FactoryPathName}",
        tags=[AppPathConstants.FactoryTagName],
    )
    app.include_router(
        WorkshopApi().router,
        prefix=f"/{AppPathConstants.WorkshopPathName}",
        tags=[AppPathConstants.WorkshopTagName],
    )
    app.include_router(
        MaterialApi().router,
        prefix=f"/{AppPathConstants.MaterialPathName}",
        tags=[AppPathConstants.MaterialTagName],
    )
    app.include_router(
        WorkshopScheduleApi().router,
        prefix=f"/{AppPathConstants.WorkshopSchedulePathName}",
        tags=[AppPathConstants.WorkshopScheduleTagName],
    )
    app.include_router(
        UserApi().router,
        prefix=f"/{AppPathConstants.UserPathName}",
        tags=[AppPathConstants.UserTagName],
    )
    app.include_router(
        TestApi().router,
        prefix=f"/test",
        tags=["Тестовые API"],
    )
