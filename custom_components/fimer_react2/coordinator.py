from datetime import timedelta
import aiohttp
import async_timeout
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, URL, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class FimerReact2Coordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(10):
                session = aiohttp.ClientSession()
                async with session.get(URL) as response:
                    data = await response.json()
                    await session.close()
                    return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")
