DOMAIN = "fimer_react2"
SCAN_INTERVAL = 30

SENSORS = {
    # Misure live
    "home_balance": {"name": "Home Balance", "unit": "Wh", "icon": "mdi:home", "device_class": "energy"},
    "generation_balance": {"name": "Generation Balance", "unit": "Wh", "icon": "mdi:solar-power", "device_class": "energy"},
    "generation_today": {"name": "Generation Today", "unit": "Wh", "icon": "mdi:solar-power", "device_class": "energy"},
    "grid_balance": {"name": "Grid Balance", "unit": "Wh", "icon": "mdi:transmission-tower", "device_class": "energy"},
    "home_today": {"name": "Home Today", "unit": "Wh", "icon": "mdi:home", "device_class": "energy"},
    "to_grid_today": {"name": "ToGrid Today", "unit": "Wh", "icon": "mdi:transmission-tower-export", "device_class": "energy"},
    
    # Stato batteria
    "battery_status": {"name": "Battery Status", "unit": "%", "icon": "mdi:battery-medium", "device_class": "battery"},
    "battery_1_charge": {"name": "Battery 1 Charge", "unit": "Wh", "icon": "mdi:battery-plus-outline", "device_class": "energy"},
    "battery_2_charge": {"name": "Battery 2 Charge", "unit": "Wh", "icon": "mdi:battery-plus-outline", "device_class": "energy"},
    "battery_1_discharge": {"name": "Battery 1 Discharge", "unit": "Wh", "icon": "mdi:battery-minus-outline", "device_class": "energy"},
    "battery_2_discharge": {"name": "Battery 2 Discharge", "unit": "Wh", "icon": "mdi:battery-minus-outline", "device_class": "energy"},
    "battery_charge_today": {"name": "Battery Charge Today", "unit": "Wh", "icon": "mdi:battery-plus", "device_class": "energy"},
    "battery_discharge_today": {"name": "Battery Discharge Today", "unit": "Wh", "icon": "mdi:battery-minus", "device_class": "energy"},

    # Flussi realtime
    "rt_generation_to_grid": {"name": "RT Generation to Grid", "unit": "Wh", "icon": "mdi:solar-panel-large", "device_class": "energy"},
    "rt_grid_to_house": {"name": "RT Grid to House", "unit": "Wh", "icon": "mdi:transmission-tower", "device_class": "energy"},
    "rt_battery_to_house": {"name": "RT Battery to House", "unit": "Wh", "icon": "mdi:battery-medium", "device_class": "energy"},
    "rt_generation_to_battery": {"name": "RT Generation to Battery", "unit": "Wh", "icon": "mdi:solar-panel-large", "device_class": "energy"},
    "generation_to_house": {"name": "Generation to House", "unit": "Wh", "icon": "mdi:solar-panel-large", "device_class": "energy"},
}
