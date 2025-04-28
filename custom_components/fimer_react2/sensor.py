from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from .const import DOMAIN

SENSORS = {
    "Home Balance": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:home-lightning-bolt",
    },
    "Generation Balance": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:solar-power",
    },
    "Generation Today": {
        "unit": "Wh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:solar-panel-large",
    },
    "Battery Status": {
        "unit": "%",
        "device_class": "battery",
        "state_class": "measurement",
        "icon": "mdi:battery",
    },
    "Generation to House": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:solar-panel",
    },
    "RT Generation to Grid": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:transmission-tower-export",
    },
    "RT Grid to House": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:transmission-tower-import",
    },
    "RT Battery to House": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:battery-arrow-down",
    },
    "RT Generation to Battery": {
        "unit": "W",
        "device_class": None,
        "state_class": "measurement",
        "icon": "mdi:battery-arrow-up",
    },
    "Grid Balance": {
        "unit": "Wh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:transmission-tower",
    },
    "Home Today": {
        "unit": "Wh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:home",
    },
    "ToGrid Today": {
        "unit": "Wh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:home-export-outline",
    },
    "Battery Charge Today": {
        "unit": "Wh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:battery-plus",
    },
    "Battery Discharge Today": {
        "unit": "Wh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:battery-minus",
    },
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]  # coordinator è un oggetto, non un dizionario
    meter_id = coordinator.meter_id
    inverter_id = coordinator.inverter_id
    battery_ids = coordinator.battery_ids

    # Raggruppiamo tutti i sensori sotto il dispositivo "Fimer REACT2"
    device_info = {
        "identifiers": {(DOMAIN, config_entry.entry_id)},
        "name": "Fimer REACT2",
        "manufacturer": "Fimer",
        "model": "REACT2",
        "sw_version": "1.0.0",  # Versione del firmware dell'inverter, se disponibile
    }

    entities = []

    for name, key, device_type, unit, device_class, state_class in SENSORS:
        if device_type == "meter":
            device_id = meter_id
        elif device_type == "inverter":
            device_id = inverter_id
        elif device_type == "battery":
            for batt_id in battery_ids:
                entities.append(FimerSensor(coordinator, batt_id, name.replace("Battery", f"Battery {batt_id[-4:]}"), key, unit, device_class, state_class, device_info))
            continue
        else:
            continue

        entities.append(FimerSensor(coordinator, device_id, name, key, unit, device_class, state_class, device_info))

    async_add_entities(entities)

class FimerSensor(SensorEntity):
    def __init__(self, coordinator, device_id, name, key, unit, device_class, state_class, device_info):
        self.coordinator = coordinator
        self.device_id = device_id
        self._attr_name = name
        self.key = key
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_device_info = device_info  # Qui assegniamo il dispositivo a cui appartiene il sensore

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
