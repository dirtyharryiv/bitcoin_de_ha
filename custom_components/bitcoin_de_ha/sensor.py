"""Custom component for tracking bitcoin.de currencies."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.config_entries import (
    ConfigEntry,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_platforms,
)
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_AVAIL,
    ATTR_EUR_BAL,
    ATTR_EUR_RATE,
    ATTR_RESERV,
    ATTR_TOTAL,
    DOMAIN,
)
from .coordinator import BitcoinDeCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Bitcoin.de balance sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    currencies: list[str] = entry.options.get(
        "currencies", entry.data.get("currencies", [])
    )

    sensors: list[SensorEntity] = [
        CryptoBalanceSensor(coordinator, currency) for currency in currencies
    ]

    sensors.append(BitcoinDeTotalBalanceSensor(coordinator))

    async_add_entities(sensors, update_before_add=True)

    entry.async_on_unload(entry.add_update_listener(async_force_reload))


async def async_force_reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Force full reload by unloading and reloading the entry."""
    entity_registry = async_get_entity_registry(hass)

    entities_to_remove = [
        entity.entity_id
        for entity in entity_registry.entities.values()
        if entity.config_entry_id == entry.entry_id
    ]

    for entity_id in entities_to_remove:
        entity_registry.async_remove(entity_id)

    await hass.config_entries.async_unload(entry.entry_id)

    entity_platforms = async_get_platforms(hass, entry.domain)

    sensor_platform = next(
        (platform for platform in entity_platforms if platform.domain == "sensor"), None
    )

    if sensor_platform is None:
        return

    async_add_entities = sensor_platform.async_add_entities

    coordinator = hass.data[DOMAIN][entry.entry_id]
    currencies: list[str] = entry.options.get(
        "currencies", entry.data.get("currencies", [])
    )

    sensors: list[SensorEntity] = [
        CryptoBalanceSensor(coordinator, currency) for currency in currencies
    ]

    sensors.append(BitcoinDeTotalBalanceSensor(coordinator))

    await async_add_entities(sensors, update_before_add=True)


class CryptoBalanceSensor(CoordinatorEntity, SensorEntity):
    """Sensor to represent cryptocurrency balance."""

    def __init__(self, coordinator: BitcoinDeCoordinator, currency: str) -> None:
        """Initialize the Bitcoin.de API Sensor."""
        super().__init__(coordinator)
        self._currency = currency.upper()
        self._attr_unique_id = f"bitcoin_de_{self._currency.lower()}"

    @property
    def name(self) -> str:
        """Return the currencies name from bitcoin.de API."""
        return f"Bitcoin.de {self._currency} Balance"

    @property
    def state(self) -> float:
        """Return the currencies total amount from bitcoin.de API."""
        return float(
            self.coordinator.data.get("balances", {})
            .get(self._currency.lower(), {})
            .get(ATTR_TOTAL, 0)
        )

    @property
    def unit_of_measurement(self) -> str:
        """Return currency symbol from bitcoin.de API."""
        return self._currency

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes from bitcoin.de API."""
        balance = self.coordinator.data.get("balances", {}).get(
            self._currency.lower(), {}
        )
        rate = (
            self.coordinator.data.get("eur_rates", {})
            .get(self._currency.lower(), {})
            .get("rate_weighted", 0)
        )
        total_amount = float(balance.get(ATTR_TOTAL, 0))
        return {
            ATTR_AVAIL: float(balance.get(ATTR_AVAIL, 0)),
            ATTR_RESERV: float(balance.get(ATTR_RESERV, 0)),
            ATTR_TOTAL: total_amount,
            ATTR_EUR_RATE: float(rate),
            ATTR_EUR_BAL: float(rate) * total_amount,
        }


class BitcoinDeTotalBalanceSensor(SensorEntity):
    """Sensor for the total balance in EUR."""

    def __init__(self, coordinator: BitcoinDeCoordinator) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Bitcoin.de Total Balance EUR"
        self._attr_unique_id = "bitcoin_de_total_balance"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_native_unit_of_measurement = "EUR"

    @property
    def state(self) -> float:
        """Return the total balance in EUR."""
        return self.coordinator.data.get("total_balance_eur", 0.0)
