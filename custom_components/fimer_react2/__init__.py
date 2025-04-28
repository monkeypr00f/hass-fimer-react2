from .const import DOMAIN
from .config_flow import FimerConfigFlow

async def async_setup_entry(hass, config_entry):
    hass.data.setdefault(DOMAIN, {})
    from .coordinator import FimerDataUpdateCoordinator

    coordinator = FimerDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    # Questo è il fix corretto
    await hass.config_entries.async_forward_entry_setup(config_entry, "sensor")

    return True

async def async_unload_entry(hass, config_entry):
    await hass.config_entries.async_unload_platforms(config_entry, ["sensor"])
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True
