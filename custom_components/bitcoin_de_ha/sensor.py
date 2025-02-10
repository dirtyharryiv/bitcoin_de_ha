"""Custom component for tracking bitcoin.de currencies."""

from homeassistant.config_entries import (
    ConfigEntry,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_platforms,
)
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BitcoinDeCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Bitcoin.de balance sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    currencies: list[str] = entry.options.get(
        "currencies", entry.data.get("currencies", [])
    )

    sensors = [CryptoBalanceSensor(coordinator, currency) for currency in currencies]

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

    sensors = [CryptoBalanceSensor(coordinator, currency) for currency in currencies]

    await async_add_entities(sensors, update_before_add=True)


class CryptoBalanceSensor(CoordinatorEntity, Entity):
    """Sensor to represent cryptocurrency balance."""

    def __init__(self, coordinator: BitcoinDeCoordinator, currency: str) -> None:
        """Initialize the Bitcoin.de API Sensor."""
        super().__init__(coordinator)
        self._currency = currency.upper()
        self._attr_unique_id = f"bitcoin_de_{self._currency.lower()}"

    @property
    def name(self) -> str:
        """Return the currencys name from bitcoin.de API."""
        return f"Bitcoin.de {self._currency} Balance"

    @property
    def state(self) -> float:
        """Return the currencys total amount from bitcoin.de API."""
        return float(
            self.coordinator.data.get(self._currency.lower(), {}).get("total_amount", 0)
        )

    @property
    def unit_of_measurement(self) -> str:
        """Return currency symbol from bitcoin.de API."""
        return self._currency

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes from bitcoin.de API."""
        balance = self.coordinator.data.get(self._currency.lower(), {})
        return {
            "available_amount": float(balance.get("available_amount", 0)),
            "reserved_amount": float(balance.get("reserved_amount", 0)),
            "total_amount": float(balance.get("total_amount", 0)),
        }
