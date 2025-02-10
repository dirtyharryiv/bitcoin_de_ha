"""Custom integration for bitcoin.de API."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import BitcoinDeCoordinator

__version__ = "1.1.0"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up currency entities from a config entry."""
    _LOGGER.info("Bitcoin.de API Integration Version: %s", __version__)
    hass.data.setdefault(DOMAIN, {})
    session = async_get_clientsession(hass)
    coordinator = BitcoinDeCoordinator(
        hass,
        session,
        entry.data["api_key"],
        entry.data["api_secret"],
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
