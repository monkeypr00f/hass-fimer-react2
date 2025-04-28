from datetime import timedelta
import aiohttp
import async_timeout
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class FimerReact2Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry):
        self.hass = hass
        self.config_entry = config_entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        host = self.config_entry.data[CONF_HOST]
        username = self.config_entry.data.get(CONF_USERNAME, "Admin")
        password = self.config_entry.data.get(CONF_PASSWORD, "00000000")

        url = f"http://{host}/v1/livedata/"

        try:
            async with async_timeout.timeout(10):
                auth = aiohttp.BasicAuth(username, password)
                session = aiohttp.ClientSession()
                async with session.get(url, auth=auth) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"HTTP error {response.status}")
                    data = await response.json()
                    await session.close()
                    return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")
