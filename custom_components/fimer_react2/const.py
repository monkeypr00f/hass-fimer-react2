DOMAIN = "fimer_react2"
SCAN_INTERVAL = 30

# Sensori statici (fissi, che sappiamo sempre esserci)
STATIC_SENSORS = {
    "home_balance": {"name": "Home Balance", "unit": "Wh", "icon": "mdi:home", "state_class": "measurement"},
    "generation_balance": {"name": "Generation Balance", "unit": "Wh", "icon": "mdi:solar-power", "state_class": "measurement"},
    "generation_today": {"name": "Generation Today", "unit": "Wh", "icon": "mdi:solar-power", "device_class": "energy", "state_class": "total_increasing"},
    "grid_balance": {"name": "Grid Balance", "unit": "Wh", "icon": "mdi:transmission-tower", "device_class": "energy", "state_class": "total_increasing"},
    "home_today": {"name": "Home Today", "unit": "Wh", "icon": "mdi:home", "device_class": "energy", "state_class": "total_increasing"},
    "to_grid_today": {"name": "To Grid Today", "unit": "Wh", "icon": "mdi:transmission-tower-export", "device_class": "energy", "state_class": "total_increasing"},
    "battery_status": {"name": "Battery Status", "unit": "%", "icon": "mdi:battery-medium", "device_class": "battery"},
    "battery_charge_today": {"name": "Battery Charge Today", "unit": "Wh", "icon": "mdi:battery-plus", "device_class": "energy", "state_class": "total_increasing"},
    "battery_discharge_today": {"name": "Battery Discharge Today", "unit": "Wh", "icon": "mdi:battery-minus", "device_class": "energy", "state_class": "total_increasing"},
    "rt_generation_to_grid": {"name": "RT Generation to Grid", "unit": "Wh", "icon": "mdi:solar-panel-large", "state_class": "measurement"},
    "rt_grid_to_house": {"name": "RT Grid to House", "unit": "Wh", "icon": "mdi:transmission-tower", "state_class": "measurement"},
    "rt_battery_to_house": {"name": "RT Battery to House", "unit": "Wh", "icon": "mdi:battery-medium", "state_class": "measurement"},
    "rt_generation_to_battery": {"name": "RT Generation to Battery", "unit": "Wh", "icon": "mdi:solar-panel-large", "device_class": "energy", "state_class": "measurement"},
    "generation_to_house": {"name": "Generation to House", "unit": "Wh", "icon": "mdi:solar-panel-large", "state_class": "measurement"},
}

# Template per sensori dinamici di ogni batteria (creati a runtime)
BATTERY_SENSOR_TYPES = {
    "charge": {"unit": "Wh", "icon": "mdi:battery-plus-outline", "state_class": "measurement"},
    "discharge": {"unit": "Wh", "icon": "mdi:battery-minus-outline", "state_class": "measurement"},
}
