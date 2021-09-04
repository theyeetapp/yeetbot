from utilities.crypto import record as record_crypto, add as add_crypto
from utilities.api import fetch_symbols as fetch_user_symbols
from utilities.error import send_error_response
import requests
import config
import sys


def update_crypto(context):
    try:
        response = fetch_user_symbols("crypto")
    except Exception:
        exception = sys.exc_info()
        return send_error_response(None, None, exception)

    symbols = response.get("symbols")
    symbols = list(map(lambda symbol: symbol["company"], symbols))
    fetch_symbols(symbols)


def fetch_symbols(all_symbols):
    i = 0
    api_endpoint = config.get().get("crypto_api_endpoint")

    while i < len(all_symbols):
        end_index = int(((i / 50) + 1) * 50)
        symbols = all_symbols[i:end_index]
        symbols = ",".join(symbols)
        try:
            response = requests.get(
                api_endpoint,
                params={
                    "ids": symbols,
                    "vs_currencies": "usd",
                    "include_market_cap": "true",
                    "include_24hr_vol": "true",
                    "include_24hr_change": "true",
                },
            )
            response.raise_for_status()
        except Exception:
            exception = sys.exc_info()
            return send_error_response(None, None, exception)

        parse_crypto_response(response.json(), i == 0)
        i += 50


def parse_crypto_response(response, record=True):
    recorded_data = dict()

    for symbol, data in response.items():
        content = {
            "price": "{:,}".format(round(data["usd"], 4)),
            "market cap": "{:,}".format(round(data["usd_market_cap"], 4)),
            "24hr volume": "{:,}".format(round(data["usd_24h_vol"], 4)),
            "24hr change": "{:,}".format(round(data["usd_24h_change"], 4)),
        }
        recorded_data[symbol] = content

    if record:
        record_crypto(recorded_data)
    else:
        add_crypto(recorded_data)
