"""Config Flow for Bitcoin.de API."""

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
)

from .const import DOMAIN


class SpotStationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bitcoin.de API."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._api_key = None
        self._api_secret = None

    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Handle the user input for the configuration."""
        errors = {}

        if user_input is not None:
            self._api_key = user_input["api_key"]
            self._api_secret = user_input["api_secret"]

            return self.async_create_entry(
                title="Bitcoin.de API",
                data={
                    "api_key": self._api_key,
                    "api_secret": self._api_secret,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "api_key",
                    ): str,
                    vol.Required(
                        "api_secret",
                    ): str,
                }
            ),
            errors=errors,
        )
