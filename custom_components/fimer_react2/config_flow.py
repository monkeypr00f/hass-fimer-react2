from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN

class FimerReact2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Fimer REACT2", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema()
        )

    def _get_schema(self):
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol

        return vol.Schema({
            vol.Required(CONF_HOST): cv.string,
            vol.Optional(CONF_USERNAME, default="Admin"): cv.string,
            vol.Optional(CONF_PASSWORD, default="00000000"): cv.string,
        })
