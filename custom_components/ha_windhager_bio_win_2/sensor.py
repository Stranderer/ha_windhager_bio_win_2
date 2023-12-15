"""Sensor platform for ha_windhager_bio_win_2."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
    UnitOfTemperature,
)
from .const import DOMAIN, LOGGER
from .coordinator import BioWin2TouchDataUpdateCoordinator
from .entity import BioWin2Entity

ENTITY_DESCRIPTIONS = [
    {
        "oid": "0/0/0/0/0/0/0/0",
        "descr": SensorEntityDescription(
            key="bioWin2_Sensor",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT,
            unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
    },
]


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        BioWin2Sensor(
            coordinator=coordinator,
            entity_description=entity_description["descr"],
            oid=entity_description["oid"],
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BioWin2Sensor(BioWin2Entity, SensorEntity):
    """ha_windhager_bio_win_2 Sensor class."""

    def __init__(
        self,
        coordinator: BioWin2TouchDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        oid: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, oid)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        LOGGER.debug(self.coordinator.data.get("OID"))
        return self.coordinator.data.get("value")
