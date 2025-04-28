from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, SENSORS

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for key, description in SENSORS.items():
        entities.append(FimerReact2Sensor(coordinator, key, description))

    async_add_entities(entities)

class FimerReact2Sensor(SensorEntity):
    def __init__(self, coordinator, key, description):
        self.coordinator = coordinator
        self._key = key
        self._description = description

    @property
    def name(self):
        return self._description["name"]

    @property
    def unique_id(self):
        return f"{self.coordinator.config_entry.entry_id}_{self._key}"

    @property
    def state(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self._key)

    @property
    def unit_of_measurement(self):
        return self._description.get("unit")

    @property
    def icon(self):
        return self._description.get("icon")

    @property
    def device_class(self):
        return self._description.get("device_class")

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        await self.coordinator.async_request_refresh()
