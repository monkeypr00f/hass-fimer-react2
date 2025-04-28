from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from .const import DOMAIN

SENSORS = [
    ("Home balance", "HousePgrid_Tot", "meter", "Wh", None, "measurement"),
    ("Generation Balance", "Pin", "inverter", "Wh", None, "measurement"),
    ("Generation Today", "Ein_runtime", "inverter", "Wh", "energy", "total_increasing"),
    ("Grid Balance", "E8_runtime", "meter", "Wh", "energy", "total_increasing"),
    ("Home Today", "E7_runtime", "meter", "Wh", "energy", "total_increasing"),
    ("ToGrid Today", "E3_runtime", "meter", "Wh", "energy", "total_increasing"),
    ("Battery status", "TSoc", "inverter", PERCENTAGE, None, "measurement"),
    ("Battery Charge Today", "ECharge_runtime", "battery", "Wh", "energy", "total_increasing"),
    ("Battery Discharge Today", "EDischarge_runtime", "battery", "Wh", "energy", "total_increasing"),
]

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    meter_id = hass.data[DOMAIN][config_entry.entry_id]["meter_id"]
    inverter_id = hass.data[DOMAIN][config_entry.entry_id]["inverter_id"]
    battery_ids = hass.data[DOMAIN][config_entry.entry_id]["battery_ids"]

    entities = []

    for name, key, device_type, unit, device_class, state_class in SENSORS:
        if device_type == "meter":
            device_id = meter_id
        elif device_type == "inverter":
            device_id = inverter_id
        elif device_type == "battery":
            for batt_id in battery_ids:
                entities.append(FimerSensor(coordinator, batt_id, name.replace("Battery", f"Battery {batt_id[-4:]}"), key, unit, device_class, state_class))
            continue
        else:
            continue

        entities.append(FimerSensor(coordinator, device_id, name, key, unit, device_class, state_class))

    async_add_entities(entities)

class FimerSensor(SensorEntity):
    def __init__(self, coordinator, device_id, name, key, unit, device_class, state_class):
        self.coordinator = coordinator
        self.device_id = device_id
        self._attr_name = name
        self.key = key
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @property
    def unique_id(self):
        return f"{self.device_id}_{self.key}"

    @property
    def native_value(self):
        data = self.coordinator.data.get(self.device_id, {}).get("points", [])
        for point in data:
            if point["name"] == self.key:
                return round(point["value"], 1)
        return None

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
