from app.seeders.factory_seeder import FactorySeeder
from app.seeders.material_seeder import MaterialSeeder
from app.seeders.operation_seeder import OperationSeeder
from app.seeders.order_status_seeder import OrderStatusSeeder
from app.seeders.organization_seeder import OrganizationSeeder
from app.seeders.organization_type_seeder import OrganizationTypeSeeder
from app.seeders.role_seeder import RoleSeeder
from app.seeders.user_seeder import UserSeeder
from app.seeders.user_type_seeder import UserTypeSeeder
from app.seeders.vehicle_category_seeder import VehicleCategorySeeder
from app.seeders.vehicle_color_seeder import VehicleColorSeeder
from app.seeders.vehicle_seeder import VehicleSeeder
from app.seeders.workshop_schedule_seeder import WorkshopScheduleSeeder
from app.seeders.workshop_seeder import WorkshopSeeder

seeders = [
    RoleSeeder(),
    OrganizationTypeSeeder(),
    UserTypeSeeder(),
    FactorySeeder(),
    WorkshopSeeder(),
    MaterialSeeder(),
    VehicleColorSeeder(),
    VehicleCategorySeeder(),
    OrderStatusSeeder(),
    WorkshopScheduleSeeder(),
    OperationSeeder(),
    UserSeeder(),
    OrganizationSeeder(),
    VehicleSeeder(),
]
