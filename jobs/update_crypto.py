from requests.exceptions import HTTPError
from utilities.crypto import record as record_crypto
import requests
import config


def update_crypto(context):
    api_endpoint = config.get().get("crypto_api_endpoint")
    crypto = fetch_formatted_crypto()

    try:
        response = requests.get(
            api_endpoint,
            params={
                "ids": crypto,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
            },
        )
        response.raise_for_status()
        record_crypto(response.json())
    except HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)


def fetch_formatted_crypto():
    db = config.get().get("db")
    cursor = db.cursor()
    query = 'SELECT company FROM symbols WHERE type="crypto"'
    cursor.execute(query)
    crypto = cursor.fetchall()
    return ",".join(list(map(lambda x: str(x[0]), crypto)))
