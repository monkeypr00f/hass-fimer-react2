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
                    raw_data = await response.json()
                    await session.close()

                    return self._parse_data(raw_data)

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

    def _parse_data(self, raw_data):
        """Parse the JSON into the expected format dynamically."""
        try:
            parsed = {}

            grid_meter_id = None
            inverter_id = None
            battery_ids = []

            # Fase 1: individua i dispositivi in base alla struttura dati
            for dev_id, dev_data in raw_data.items():
                points = dev_data.get("points", [])
                if len(points) >= 80:
                    inverter_id = dev_id
                elif len(points) >= 30:
                    grid_meter_id = dev_id
                elif len(points) >= 20:
                    battery_ids.append(dev_id)

            if not grid_meter_id or not inverter_id:
                _LOGGER.error("Cannot find grid meter or inverter in data")
                return {}

            # Fase 2: Estrai i dati dai device identificati
            parsed["home_balance"] = round(raw_data[grid_meter_id]["points"][7]["value"], 1)
            parsed["generation_balance"] = round(raw_data[inverter_id]["points"][10]["value"], 1)
            parsed["generation_today"] = round(raw_data[inverter_id]["points"][67]["value"], 1)
            parsed["grid_balance"] = round(raw_data[grid_meter_id]["points"][34]["value"], 1)
            parsed["home_today"] = round(raw_data[grid_meter_id]["points"][31]["value"], 1)
            parsed["to_grid_today"] = round(raw_data[grid_meter_id]["points"][25]["value"], 1)

            parsed["battery_status"] = round(raw_data[inverter_id]["points"][79]["value"], 1)

            charge_values = []
            discharge_values = []

            for bat_id in battery_ids:
                charge = round(raw_data[bat_id]["points"][23]["value"], 1)
                discharge = round(raw_data[bat_id]["points"][19]["value"], 1)
                parsed[f"{bat_id}_charge"] = charge
                parsed[f"{bat_id}_discharge"] = discharge
                charge_values.append(charge)
                discharge_values.append(discharge)

            parsed["battery_charge_today"] = sum(charge_values)
            parsed["battery_discharge_today"] = sum(discharge_values)

            self.battery_name_map = {
                dev_id: f"Battery {i+1}"
                for i, dev_id in enumerate(battery_ids)
            }
            
            rt_grid = round(raw_data[grid_meter_id]["points"][18]["value"], 1)
            if rt_grid >= 0:
                parsed["rt_generation_to_grid"] = rt_grid
                parsed["rt_grid_to_house"] = 0
            else:
                parsed["rt_generation_to_grid"] = 0
                parsed["rt_grid_to_house"] = abs(rt_grid)

            battery_flow = round(raw_data[inverter_id]["points"][78]["value"], 1)
            if battery_flow >= 0:
                # Positivo = Batteria sta scaricando verso casa
                parsed["rt_generation_to_battery"] = 0
                parsed["rt_battery_to_house"] = battery_flow
            else:
                # Negativo = FV sta caricando la batteria
                parsed["rt_generation_to_battery"] = abs(battery_flow)
                parsed["rt_battery_to_house"] = 0

            inverter_pin = round(raw_data[inverter_id]["points"][10]["value"], 1)
            to_battery = round(raw_data[inverter_id]["points"][78]["value"], 1)
            if to_battery < inverter_pin:
                parsed["generation_to_house"] = abs(inverter_pin + to_battery)
            else:
                parsed["generation_to_house"] = abs(inverter_pin)

            parsed["inverter_temperature"] = round(raw_data[inverter_id]["points"][23]["value"], 1)  # TempInv
            for idx, bat_id in enumerate(battery_ids):
                tba = raw_data[bat_id]["points"][4]["value"]  # Tba
                parsed[f"battery_{idx+1}_temperature"] = round(tba, 1)

            return parsed

        except Exception as err:
            _LOGGER.error(f"Error parsing data: {err}")
            return {}
