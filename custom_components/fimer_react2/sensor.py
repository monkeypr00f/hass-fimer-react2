from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, STATIC_SENSORS, BATTERY_SENSOR_TYPES

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []

    # Sensori statici (li creiamo SEMPRE subito)
    for key, description in STATIC_SENSORS.items():
        entities.append(FimerReact2Sensor(coordinator, key, description))

    async_add_entities(entities)

    # Ora aspettiamo i dati per i sensori dinamici
    if not coordinator.data:
        await coordinator.async_request_refresh()

    # Sensori dinamici batterie
    battery_entities = []
    for key in coordinator.data.keys():
        if "_charge" in key or "_discharge" in key:
            battery_id, sensor_type = key.split("_", 1)
            sensor_info = BATTERY_SENSOR_TYPES.get(sensor_type)
            if sensor_info:
                description = {
                    "name": f"{battery_id} {sensor_type.capitalize()}",
                    "unit": sensor_info["unit"],
                    "icon": sensor_info["icon"],
                    "device_class": sensor_info["device_class"],
                }
                battery_entities.append(FimerReact2Sensor(coordinator, key, description))

    async_add_entities(battery_entities)

class FimerReact2Sensor(SensorEntity):
    def __init__(self, coordinator, key, description):
        self.coordinator = coordinator
        self._key = key
        self._description = description

    @property
    def name(self):
        return self._description.get("name")

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

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.config_entry.entry_id)},
            "name": "Fimer REACT2",
            "manufacturer": "Fimer",
            "model": "REACT2",
            "entry_type": "service",
        }

    async def async_update(self):
        await self.coordinator.async_request_refresh()
