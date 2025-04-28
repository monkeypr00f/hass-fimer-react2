from .const import DOMAIN
from .coordinator import FimerReact2Coordinator

async def async_setup_entry(hass, config_entry):
    coordinator = FimerReact2Coordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])

    return True

async def async_unload_entry(hass, config_entry):
    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])

    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True
