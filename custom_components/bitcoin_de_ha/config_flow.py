"""Config Flow for Bitcoin.de API."""

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
)

from .const import AVAILABLE_CURRENCIES, DOMAIN


class BitcoinDeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bitcoin.de API."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._api_key = None
        self._api_secret = None
        self._currencies = None

    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Handle the user input for the configuration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._api_key = user_input["api_key"]
            self._api_secret = user_input["api_secret"]
            self._currencies = user_input["currencies"]

            return self.async_create_entry(
                title="Bitcoin.de API",
                data={
                    "api_key": self._api_key,
                    "api_secret": self._api_secret,
                    "currencies": self._currencies,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                    vol.Required("api_secret"): str,
                    vol.Required("currencies", default=["btc"]): cv.multi_select(
                        AVAILABLE_CURRENCIES
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Return the options flow handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for reconfiguration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    "currencies",
                    default=self.config_entry.options.get(
                        "currencies", self.config_entry.data.get("currencies", [])
                    ),
                ): cv.multi_select(AVAILABLE_CURRENCIES)
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
