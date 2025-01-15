from typing import Optional

from app.entities import VehicleModel


class VehicleHelper:
    @staticmethod
    def get_vehicle_registration_number(vehicle:VehicleModel, trailer:Optional[VehicleModel]):
        if trailer:
            return f"{vehicle.registration_number}/{trailer.registration_number}"
        return vehicle.registration_number