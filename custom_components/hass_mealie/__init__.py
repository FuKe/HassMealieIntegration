from homeassistant import core
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_TOKEN, CONF_URL
from homeassistant.core import HomeAssistant


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Mealie Integration component."""
    # @TODO: Add setup code.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """ Setup Mealie Integration from a config entry """
    api_key = entry.data[CONF_API_TOKEN]
    mealie_base_url = entry.data[CONF_URL]