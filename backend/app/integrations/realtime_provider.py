from typing import Protocol

from app.domain.vehicle import VehicleState


class RealtimeVehicleProvider(Protocol):
    async def get_vehicles(self) -> list[VehicleState]:
        """Return normalized vehicles while preserving vehicle and trip IDs."""
