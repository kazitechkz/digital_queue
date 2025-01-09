from pathlib import Path
from typing import Annotated

from app.shared.field_constants import FieldConstants


class AppPathConstants:
    IDPath = Annotated[int, Path(gt=0, description="Уникальный идентификатор")]
    ValuePath = Annotated[
        str,
        Path(
            max_length=FieldConstants.STANDARD_LENGTH, description="Уникальное значение"
        ),
    ]

    RolePathName = "role"
    RoleTagName = "Роли"
    UserTypePathName = "user-type"
    UserTypeTagName = "Тип пользователя"
    FilePathName = "file"
    FileTagName = "Файлы и файловая система"
    OrganizationTypePathName = "organization-type"
    OrganizationTypeTagName = "Тип организации"
    VehicleColorPathName = "vehicle-color"
    VehicleColorTagName = "Цвет транспортного средства"
    VehicleCategoryPathName = "vehicle-category"
    VehicleCategoryTagName = "Категория транспортного средства"
    OrderStatusPathName = "order-status"
    OrderStatusTagName = "Статус заказа"
    OrderPathName = "order"
    OrderTagName = "Заказы"
    OperationPathName = "operation"
    OperationTagName = "Бизнес процесс"
    FactoryPathName = "factory"
    FactoryTagName = "Заводы"
    WorkshopPathName = "workshop"
    WorkshopTagName = "Цеха"
    MaterialPathName = "material"
    MaterialTagName = "Материал"
    WorkshopSchedulePathName = "workshop-schedule"
    WorkshopScheduleTagName = "Расписание Цеха"
    UserPathName = "user"
    UserTagName = "Пользователи"
    OrganizationPathName = "organization"
    OrganizationTagName = "Организации"
    VehiclePathName = "vehicle"
    VehicleTagName = "Транспортные средства (ТС)"
    VerifiedUserPathName = "verified-user"
    VerifiedUserTagName = "Подтвержденные пользователи"
    VerifiedVehiclePathName = "verified-vehicle"
    VerifiedVehicleTagName = "Подтвержденные транспортные средства (ТС)"
    OrganizationEmployeePathName = "organization-employee"
    OrganizationEmployeeTagName = "Работники Организации"
    AuthPathName = "auth"
    AuthTagName = "Аутентификация"
    TestPathName = "test"
    TestTagName = "Для тестирования"
    EmployeeRequestPathName = "employee-request"
    EmployeeRequestTagName = "Заявка на добавление в организацию"

    IndexPathName = "/"
    CreatePathName = "/create"
    UpdatePathName = "/update/{id}"
    GetByIdPathName = "/get/{id}"
    DeleteByIdPathName = "/delete/{id}"
    GetByValuePathName = "/get-by-value/{value}"

    #Client
    #Vehicles
    AddClientVehiclePathName = "/add-vehicle"
    PaginateClientVehiclesPathName = "/paginate-client-vehicles"
    GetClientVehiclesPathName = "/all-client-vehicles"
    UpdateClientVehiclePathName = "/update-client-vehicle/{id}"
    #Organization
    AddClientOrganizationPathName = "/add-client-organization"
    UpdateClientOrganizationPathName = "/update-client-organization/{id}"
    AllClientOrganizationPathName = "/all-client-organization"
    PaginateClientOrganizationPathName = "/paginate-client-organization"
    #Employee Requests
    PaginateClientEmployeeRequestPathName = "/my-employee-requests"
    CreateClientEmployeeRequestPathName = "/create-client"
    UpdateClientEmployeeRequestPathName = "/make-decision/{id}"
    DeleteClientEmployeeRequestPathName = "/delete-client/{id}"
    #Order
    CreateClientOrderRequestPathName = "/create-client-order"
    #Auth
    LoginPathName = "/login"
    GetMePathName = "/me"
