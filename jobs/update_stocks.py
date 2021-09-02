from utilities.stocks import record as record_stocks
from utilities.api import fetch_symbols
from utilities.error import send_error_response
from datetime import datetime, timedelta
import requests
import config
import sys


def update_stocks(context):
    config_dict = config.get()
    api_endpoint = config_dict.get("stocks_api_endpoint")
    api_key = config_dict.get("stocks_api_key")
    try:
        response = fetch_symbols("stock")
    except Exception:
        exception = sys.exc_info()
        return send_error_response(None, None, exception)

    symbols = response.get("symbols")
    symbols = ",".join(list(map(lambda symbol: symbol["name"], symbols)))

    try:
        response = requests.get(
            api_endpoint,
            params={
                "access_key": api_key,
                "symbols": symbols,
                "date_from": get_date(),
                "date_to": get_date(),
            },
        )
        response.raise_for_status()
        parse_stocks_response(response.json())
    except Exception:
        exception = sys.exc_info()
        return send_error_response(None, None, exception)


def parse_stocks_response(response):
    data = response["data"]
    recorded_data = dict()

    for content in data:
        symbol = content["symbol"]
        recorded_content = {
            "open": str(content["open"]),
            "high": str(content["high"]),
            "low": str(content["low"]),
            "close": str(content["close"]),
            "volume": str(content["volume"]),
        }
        recorded_data[symbol] = recorded_content

    record_stocks(recorded_data)


def get_date():
    dt = datetime.today() - timedelta(days=1)
    return dt.strftime("%Y-%m-%d")
