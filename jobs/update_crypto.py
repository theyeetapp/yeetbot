from requests.exceptions import HTTPError
from utilities.crypto import record as record_crypto
from utilities.api import fetch_symbols
from requests.exceptions import HTTPError
import requests
import config


def update_crypto(context):
    api_endpoint = config.get().get("crypto_api_endpoint")

    try:
        response = fetch_symbols("crypto")
    except HTTPError as error:
        print(error)
    except Exception as error:
        print(error)

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
    except HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)

    record_crypto(response.json())
