"""BlueprintEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION
from .coordinator import BioWin2TouchDataUpdateCoordinator


class BioWin2Entity(CoordinatorEntity):
    """BioWin2Entity class."""

    def __init__(self, coordinator: BioWin2TouchDataUpdateCoordinator, oid) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )
        self._attr_oid = oid
