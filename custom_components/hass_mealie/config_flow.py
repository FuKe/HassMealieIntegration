import logging
import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_API_TOKEN, CONF_URL
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .mealie_client import MealieClient, UnauthorizedException, ConnectionFailedException

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_API_TOKEN): str
    }
)

async def validate_input(hass: HomeAssistant, data) -> bool:
    """ Validate user input allows us to connect to the Mealie API """
    config_path = hass.config.path("custom_components/hass_mealie/mealie.conf")
    mealie_client = MealieClient(data[CONF_API_TOKEN], data[CONF_URL])
    
    result = await hass.async_add_executor_job(mealie_client.get_self)
    _LOGGER.debug(f"Resposne from get_self was: ${str(result)}")
    
    return True
    
    
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    
    async def async_step_user(self, user_input=None):
        errors = {}
        
        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
                return self.async_create_entry(title="Mealie Integration Entry", data=user_input)
            except UnauthorizedException:
                errors["base"] = "invalid_auth"
            except ConnectionFailedException:
                errors["base"] = "cannot_connect"
            except Exception as ex:
                _LOGGER.exception("User input validation failed with unknown exception", ex)
                errors["base"] = "unknown"
        
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
    
# TODO: Implement OptionsFlow to allow the user to update Mealie base url and API key