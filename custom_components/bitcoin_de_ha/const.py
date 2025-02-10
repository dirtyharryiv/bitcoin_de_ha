"""Constants for Bitcoin.de API Custom Integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "bitcoin_de_ha"
UPDATE_INTERVAL = 300
API_URL = "https://api.bitcoin.de/v4/account"
