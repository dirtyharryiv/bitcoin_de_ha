"""Custom component for tracking bitcoin.de currencies."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BitcoinDeCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Bitcoin.de balance sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        CryptoBalanceSensor(coordinator, currency)
        for currency in coordinator.data
        if float(coordinator.data[currency]["total_amount"]) > 0
    ]
    async_add_entities(sensors, update_before_add=True)


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
