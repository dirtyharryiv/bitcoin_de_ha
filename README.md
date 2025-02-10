# Bitcoin.de API Home Assistant Integration

This custom integration for Home Assistant enables you to track your cryptocurrency balances from Bitcoin.de directly within Home Assistant.

## Installation

1. **Install via HACS:**
   - [![Open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dirtyharryiv&repository=bitcoin_de_ha&category=Integration)
   - In the bottom right corner click **Download**.

1. **Manual Installation:**
   - Download or clone this repository.
   - Place the `bitcoin_de_ha` folder in your Home Assistant `custom_components` directory.
     ```bash
     /config/custom_components/bitcoin_de_ha/
     ```

1. Restart Home Assistant to load the integration.

## Configuration
1. In Home Assistant, go to **Settings > Devices & Services**.
1. Click **Add Integration** and search for **Bitcoin.de API**.
1. Enter your Bitcoin.de API Key and Secret.
1. Choose the currencies you want to retrieve.
1. Click **Submit**, and Home Assistant will start retrieving your balances.

## Entities Created
The integration dynamically generates sensors for each cryptocurrency you chose, such as:
- `sensor.bitcoin_de_btc_balance`
- `sensor.bitcoin_de_eth_balance`
- `sensor.bitcoin_de_bch_balance`

Each sensor provides the following attributes:
- **Available Amount**: Funds available for trading
- **Reserved Amount**: Funds reserved for active orders
- **Total Amount**: The total balance for the respective cryptocurrency
- **Euro Rates**: The euro rates
- **Euro Balance**: The euro balance

A total Euro balance sensor is created as well:
- `sensor.bitcoin_de_total_balance_eur`

## Troubleshooting & Support
- Ensure your API key has the necessary permissions to access balance data.
- Check Home Assistant logs for errors related to this integration.
- If you encounter issues, please open an issue on the [GitHub repository](https://github.com/dirtyharryiv/bitcoin_de_ha/issues).

## Disclaimer

This project is an independent integration and is not affiliated with, endorsed by, or supported by Bitcoin.de. Use this integration at your own risk. The author assumes no responsibility for any financial loss, API access issues, or account-related problems resulting from the use of this software.