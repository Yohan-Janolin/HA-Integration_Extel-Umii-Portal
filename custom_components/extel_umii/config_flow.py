import voluptuous as vol
import uuid
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .api import ExtelUmiiAPI
from .const import (
    DOMAIN,
    CONF_GATE_ID,
    CONF_DEVICE_ID,
    CONF_DEVICE_TOKEN,
    CONF_USER_AGENT,
    DEFAULT_USER_AGENT,
)


class ExtelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._email = None
        self._password = None
        self._device_token = None
        self._user_agent = DEFAULT_USER_AGENT
        # On génère un ID unique pour le store
        self._device_id = str(uuid.uuid4()).upper()

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self._email = user_input[CONF_EMAIL]
            self._password = user_input[CONF_PASSWORD]
            self._device_token = user_input.get(CONF_DEVICE_TOKEN)
            self._user_agent = user_input.get(CONF_USER_AGENT) or DEFAULT_USER_AGENT

            api = ExtelUmiiAPI(
                self._email,
                self._password,
                self._device_id,
                self._device_token,
                self._user_agent,
            )
            if await api.login():
                return await self.async_step_select_gate()
            errors["base"] = "Login incorrect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_DEVICE_TOKEN): str,
                vol.Optional(CONF_USER_AGENT, default=DEFAULT_USER_AGENT): str,
            }),
            errors=errors,
        )

    async def async_step_select_gate(self, user_input=None):
        api = ExtelUmiiAPI(
            self._email,
            self._password,
            self._device_id,
            self._device_token,
            self._user_agent,
        )
        await api.login()
        gates = await api.get_gates()

        if not gates:
            return self.async_abort(reason="Pas de portail trouvé")

        if user_input is not None:
            gate_id = user_input[CONF_GATE_ID]
            return self.async_create_entry(
                title=gates[gate_id],
                data={
                    CONF_EMAIL: self._email,
                    CONF_PASSWORD: self._password,
                    CONF_GATE_ID: gate_id,
                    CONF_DEVICE_ID: self._device_id,
                    CONF_DEVICE_TOKEN: self._device_token,
                    CONF_USER_AGENT: self._user_agent,
                },
            )

        return self.async_show_form(
            step_id="select_gate",
            data_schema=vol.Schema({
                vol.Required(CONF_GATE_ID): vol.In(gates)
            }),
        )