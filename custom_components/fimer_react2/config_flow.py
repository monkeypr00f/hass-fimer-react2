import logging
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("host"): str,
    vol.Required("username"): str,
    vol.Required("password"): str,
})

class FimerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.data = {}
        self.devices = {}
        self.meter_id = None
        self.inverter_id = None
        self.battery_ids = []

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Passo di configurazione iniziale: connessione all'inverter"""
        if user_input is not None:
            self.data.update(user_input)
            try:
                auth = aiohttp.BasicAuth(user_input["username"], user_input["password"])
                async with aiohttp.ClientSession(auth=auth) as session:
                    async with session.get(f"http://{user_input['host']}/v1/livedata/") as response:
                        if response.status != 200:
                            raise Exception(f"HTTP error {response.status}")
                        raw = await response.json()

                        # Classificare i dispositivi
                        for dev_id, dev_info in raw.items():
                            dev_type = dev_info.get("device_type", "")
                            if dev_type == "meter" and self.meter_id is None:
                                self.meter_id = dev_id
                            elif "inverter" in dev_type and self.inverter_id is None:
                                self.inverter_id = dev_id
                            elif dev_type == "battery":
                                self.battery_ids.append(dev_id)

                        if not self.meter_id or not self.inverter_id:
                            raise Exception("Meter o inverter non trovati!")

            except Exception as e:
                _LOGGER.error("Errore connessione o parsing inverter: %s", e)
                return self.async_show_form(
                    step_id="user",
                    data_schema=STEP_USER_DATA_SCHEMA,
                    errors={"base": "cannot_connect"},
                )

            return await self.async_step_confirm()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA
        )

    async def async_step_confirm(self, user_input=None) -> FlowResult:
        """Passo di conferma: mostra i dispositivi rilevati"""
        if user_input is not None:
            # Confermato: salviamo i dati
            self.data["meter_id"] = self.meter_id
            self.data["inverter_id"] = self.inverter_id
            self.data["battery_ids"] = self.battery_ids
            return self.async_create_entry(title="Fimer REACT2", data=self.data)

        # Mostriamo il recap dei dispositivi rilevati
        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "meter": self.meter_id,
                "inverter": self.inverter_id,
                "batteries": ", ".join(self.battery_ids) if self.battery_ids else "Nessuna"
            },
            data_schema=vol.Schema({}),
        )
