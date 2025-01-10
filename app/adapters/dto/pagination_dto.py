from typing import Generic, List, TypeVar

from pydantic import BaseModel

from app.adapters.dto.employee_request.employee_request_dto import EmployeeRequestWithRelationsDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.organization.organization_dto import \
    OrganizationWithRelationsDTO
from app.adapters.dto.organization_employee.organization_employee_dto import \
    OrganizationEmployeeWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.dto.vehicle.vehicle_dto import VehicleWithRelationsDTO
from app.adapters.dto.verified_user.verified_user_dto import \
    VerifiedUserWithRelationsDTO
from app.adapters.dto.verified_vehicle.verified_vehicle_dto import \
    VerifiedVehicleWithRelationsDTO

T = TypeVar("T")


class Pagination(Generic[T]):
    current_page: int
    last_page: int
    total_pages: int
    total_items: int
    items: list[T]

    def __init__(
        self,
        items: list[T],
        total_pages: int,
        total_items: int,
        per_page: int,
        page: int,
    ) -> None:
        self.items = items
        self.total_pages = total_pages
        self.total_items = total_items
        self.current_page = page
        self.last_page = (total_pages + per_page - 1) // per_page


class BasePageModel(BaseModel):
    current_page: int
    last_page: int
    total_pages: int
    total_items: int


class PaginationUserWithRelationsDTO(BasePageModel):
    items: list[UserWithRelationsDTO]


class PaginationFileRDTO(BasePageModel):
    items: list[FileRDTO]


class PaginationOrganizationWithRelationsDTO(BasePageModel):
    items: List[OrganizationWithRelationsDTO]


class PaginationVehicleWithRelationsDTO(BasePageModel):
    items: List[VehicleWithRelationsDTO]


class PaginationVerifiedUserWithRelationsDTO(BasePageModel):
    items: List[VerifiedUserWithRelationsDTO]


class PaginationVerifiedVehicleWithRelationsDTO(BasePageModel):
    items: List[VerifiedVehicleWithRelationsDTO]


class PaginationOrganizationEmployeeWithRelationsDTO(BasePageModel):
    items: List[OrganizationEmployeeWithRelationsDTO]

class PaginationEmployeeRequestWithRelationsDTO(BasePageModel):
    items: List[EmployeeRequestWithRelationsDTO]

class PaginationOrderWithRelationsDTO(BasePageModel):
    items: List[OrderWithRelationsDTO]