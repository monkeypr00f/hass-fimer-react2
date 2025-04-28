import asyncio
import logging
import aiohttp
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, CONF_HOST, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

class FimerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        self.hass = hass
        self.host = config[CONF_HOST]
        self.username = config[CONF_USERNAME]
        self.password = config[CONF_PASSWORD]
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from inverter."""
        auth = aiohttp.BasicAuth(self.username, self.password)
        url = f"http://{self.host}/v1/livedata/"
        try:
            async with aiohttp.ClientSession(auth=auth) as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"HTTP Error {response.status}")
                    data = await response.json()
                    return data
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout fetching data") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed("Client error fetching data") from err
