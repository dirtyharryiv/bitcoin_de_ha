# Bitcoin.de API Home Assistant Integration

This custom integration for Home Assistant enables you to track your cryptocurrency balances from Bitcoin.de directly within Home Assistant.

## Features
- Automatically retrieves your Bitcoin.de balance
- Creates entities for each cryptocurrency with a positive balance

## Installation

1. **Install via HACS:**
   - [![Open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dirtyharryiv&repository=bitcoin_de_ha&category=Integration)
   - In the bottom right corner click **Download**.

2. **Manual Installation:**
   - Download or clone this repository.
   - Place the `bitcoin_de_ha` folder in your Home Assistant `custom_components` directory.
     ```bash
     /config/custom_components/bitcoin_de_ha/
     ```

3. Restart Home Assistant to load the integration.

## Configuration
1. In Home Assistant, go to **Settings > Devices & Services**.
2. Click **Add Integration** and search for **Bitcoin.de API**.
3. Enter your Bitcoin.de API Key and Secret.
4. Click **Submit**, and Home Assistant will start retrieving your balances.

## Entities Created
The integration dynamically generates sensors for each cryptocurrency with a positive balance, such as:
- `sensor.bitcoin_de_btc_balance`
- `sensor.bitcoin_de_eth_balance`
- `sensor.bitcoin_de_bch_balance`

Each sensor provides the following attributes:
- **Available Amount**: Funds available for trading
- **Reserved Amount**: Funds reserved for active orders
- **Total Amount**: The total balance for the respective cryptocurrency

## Troubleshooting & Support
- Ensure your API key has the necessary permissions to access balance data.
- Check Home Assistant logs for errors related to this integration.
- If you encounter issues, please open an issue on the [GitHub repository](https://github.com/dirtyharryiv/bitcoin_de_ha/issues).

## Disclaimer

This project is an independent integration and is not affiliated with, endorsed by, or supported by Bitcoin.de. Use this integration at your own risk. The author assumes no responsibility for any financial loss, API access issues, or account-related problems resulting from the use of this software.