class FimerDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinatore per l'integrazione Fimer REACT2"""

    def __init__(self, hass, config_entry):
        """Inizializza il coordinatore"""
        self.hass = hass
        self.host = config_entry.data[CONF_HOST]
        self.username = config_entry.data[CONF_USERNAME]
        self.password = config_entry.data[CONF_PASSWORD]
        self.meter_id = None
        self.inverter_id = None
        self.battery_ids = []
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

                    # Estrai i dati per meter, inverter e batterie
                    for dev_id, dev_info in data.items():
                        dev_type = dev_info.get("device_type", "")
                        if dev_type == "meter" and self.meter_id is None:
                            self.meter_id = dev_id
                        elif "inverter" in dev_type and self.inverter_id is None:
                            self.inverter_id = dev_id
                        elif dev_type == "battery":
                            self.battery_ids.append(dev_id)

                    return data
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout fetching data") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed("Client error fetching data") from err
