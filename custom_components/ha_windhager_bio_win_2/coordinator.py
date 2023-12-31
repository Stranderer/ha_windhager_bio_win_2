"""DataUpdateCoordinator for ha_windhager_bio_win_2."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    BioWin2TouchApiClient,
    BioWin2TouchApiClientAuthenticationError,
    BioWin2TouchApiClientError,
)
from .const import DOMAIN, LOGGER

DEFAULT_UPDATE_INTERVAL_MINUTES = 5


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BioWin2TouchDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: BioWin2TouchApiClient,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=15),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.client.async_get_data()
        except BioWin2TouchApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except BioWin2TouchApiClientError as exception:
            raise UpdateFailed(exception) from exception
