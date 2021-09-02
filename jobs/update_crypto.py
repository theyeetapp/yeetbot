from utilities.crypto import record as record_crypto
from utilities.api import fetch_symbols
from utilities.error import send_error_response
import requests
import config
import sys


def update_crypto(context):
    api_endpoint = config.get().get("crypto_api_endpoint")

    try:
        response = fetch_symbols("crypto")
    except Exception:
        exception = sys.exc_info()
        return send_error_response(None, None, exception)

    symbols = response.get("symbols")
    symbols = ",".join(list(map(lambda symbol: symbol["company"], symbols)))

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

    parse_crypto_response(response.json())


def parse_crypto_response(response):
    recorded_data = dict()

    for symbol, data in response.items():
        content = {
            "price": "{:,}".format(round(data["usd"], 4)),
            "market cap": "{:,}".format(round(data["usd_market_cap"], 4)),
            "24hr volume": "{:,}".format(round(data["usd_24h_vol"], 4)),
            "24hr change": "{:,}".format(round(data["usd_24h_change"], 4)),
        }
        recorded_data[symbol] = content

    print(recorded_data)
    record_crypto(recorded_data)
