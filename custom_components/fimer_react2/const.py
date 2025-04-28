
DOMAIN = "fimer_react2"
SCAN_INTERVAL = 30

URL = "http://192.168.178.105/v1/livedata/"

SENSORS = {
    "home_today": {"name": "Home Today", "unit": "Wh", "icon": "mdi:home", "device_class": "energy"},
    "grid_balance": {"name": "Grid Balance", "unit": "Wh", "icon": "mdi:transmission-tower", "device_class": "energy"},
    "battery_status": {"name": "Battery Status", "unit": "%", "icon": "mdi:battery-medium", "device_class": None},
}
