from app.adapters.api.order_status.order_status_api import OrderStatusApi
from app.adapters.api.organization_type.organization_type_api import \
    OrganizationTypeApi
from app.adapters.api.role.role_api import RoleApi
from app.adapters.api.vehicle_category.vehicle_category_api import \
    VehicleCategoryApi
from app.adapters.api.vehicle_color.vehicle_color_api import VehicleColorApi
from app.shared.path_constants import AppPathConstants


def include_routers(app) -> None:
    app.include_router(
        RoleApi().router,
        prefix=f"/{AppPathConstants.RolePathName}",
        tags=[AppPathConstants.RoleTagName],
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