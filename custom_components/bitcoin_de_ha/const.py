"""Constants for Bitcoin.de API Custom Integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "bitcoin_de_ha"

UPDATE_INTERVAL = 60

API_ACCOUNT_URL = "https://api.bitcoin.de/v4/account"
API_RATES_URL = "https://api.bitcoin.de/v4/{}eur/basic/rate.json?apikey={}"

AVAILABLE_CURRENCIES = {
    "btc": "Bitcoin",
    "bch": "Bitcoin Cash",
    "btg": "Bitcoin Gold",
    "eth": "Ether",
    "ltc": "Litecoin",
    "xrp": "Ripple",
    "doge": "Dogecoin",
    "sol": "Solana",
    "trx": "Tron",
    "usdt": "Tether (ETH-Chain)",
}

ATTR_AVAIL = "available_amount"
ATTR_RESERV = "reserved_amount"
ATTR_TOTAL = "total_amount"
ATTR_EUR_RATE = "eur_rate"
ATTR_EUR_BAL = "eur_balance"
