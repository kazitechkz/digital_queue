from app.seeders.role_seeder import RoleSeeder
from app.seeders.organization_type_seeder import OrganizationTypeSeeder
from app.seeders.user_type_seeder import UserTypeSeeder

seeders = [
    RoleSeeder(),
    OrganizationTypeSeeder(),
    UserTypeSeeder(),
]
