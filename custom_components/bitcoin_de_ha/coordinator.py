"""Class to manage fetching currency data from bitcoin.de API."""

import hashlib
import hmac
import logging
import time
from datetime import timedelta

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class BitcoinDeCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Bitcoin.de API."""

    def __init__(
        self, hass: HomeAssistant, session: ClientSession, api_key: str, api_secret: str
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Bitcoin.de Balance",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.session = session
        self._api_key = api_key
        self._api_secret = api_secret

    async def _async_update_data(self) -> dict:
        nonce = str(int(time.time() * 1_000_000))
        post_parameter_md5 = hashlib.md5(b"").hexdigest()
        hmac_data = f"GET#{API_URL}#{self._api_key}#{nonce}#{post_parameter_md5}"
        signature = hmac.new(
            self._api_secret.encode(), hmac_data.encode(), hashlib.sha256
        ).hexdigest()
        headers = {
            "X-API-KEY": self._api_key,
            "X-API-NONCE": nonce,
            "X-API-SIGNATURE": signature,
        }

        try:
            async with self.session.get(API_URL, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("data", {}).get("balances", {})
        except Exception as error:
            _LOGGER.exception("Request error")
            raise UpdateFailed from error
