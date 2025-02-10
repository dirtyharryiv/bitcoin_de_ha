"""Class to manage fetching currency data from bitcoin.de API."""

import hashlib
import hmac
import logging
import time
from datetime import timedelta

from aiohttp import ClientError, ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_ACCOUNT_URL, API_RATES_URL, ATTR_TOTAL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class BitcoinDeCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Bitcoin.de API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        api_key: str,
        api_secret: str,
        currencies: list[str],
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
        self._currencies = currencies
        self.data = {"balances": {}, "eur_rates": {}, "total_balance_eur": 0.0}

    async def _async_update_data(self) -> dict:
        nonce = str(int(time.time() * 1_000_000))
        post_parameter_md5 = hashlib.md5(b"").hexdigest()
        hmac_data = (
            f"GET#{API_ACCOUNT_URL}#{self._api_key}#{nonce}#{post_parameter_md5}"
        )
        signature = hmac.new(
            self._api_secret.encode(), hmac_data.encode(), hashlib.sha256
        ).hexdigest()
        headers = {
            "X-API-KEY": self._api_key,
            "X-API-NONCE": nonce,
            "X-API-SIGNATURE": signature,
        }

        data = {}

        try:
            async with self.session.get(API_ACCOUNT_URL, headers=headers) as response:
                response.raise_for_status()
                balance_data = await response.json()
                data["balances"] = balance_data.get("data", {}).get("balances", {})

        except Exception as error:
            _LOGGER.exception("Error fetching account balance")
            raise UpdateFailed from error

        data["eur_rates"] = await self._fetch_currency_rates()
        total_balance = 0.0
        for currency, balance in data["balances"].items():
            amount = float(balance.get(ATTR_TOTAL, 0.0))
            currency_rate = data["eur_rates"].get(currency, {})

            if isinstance(currency_rate, dict):
                rate = float(currency_rate.get("rate_weighted", 0.0))
            else:
                rate = float(currency_rate)

            total_balance += amount * rate

        data["total_balance_eur"] = total_balance

        return data

    async def _fetch_currency_rates(self) -> dict[str, float]:
        """Fetch the current EUR rate for each selected currency."""
        currency_rates = {}

        for currency in self._currencies:
            url = API_RATES_URL.format(currency.lower(), self._api_key)

            try:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    rate_data = await response.json()
                    currency_rates[currency] = rate_data.get("rate", 0.0)

            except (TimeoutError, ClientError) as error:
                _LOGGER.warning("Error fetching EUR rate for %s: %s", currency, error)
                currency_rates[currency] = None

        return currency_rates
