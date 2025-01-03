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
