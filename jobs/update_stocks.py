from utilities.stocks import record as record_stocks, add as add_stocks
from utilities.api import fetch_symbols as fetch_user_symbols
from utilities.error import send_error_response
from datetime import datetime, timedelta
import requests
import config
import sys


def update_stocks(context):
    try:
        response = fetch_user_symbols("stock")
    except Exception:
        exception = sys.exc_info()
        return send_error_response(None, None, exception)

    symbols = response.get("symbols")
    symbols = list(map(lambda symbol: symbol["name"], symbols))
    fetch_symbols(symbols)


def fetch_symbols(all_symbols):
    i = 0
    config_dict = config.get()
    api_endpoint = config_dict.get("stocks_api_endpoint")
    api_key = config_dict.get("stocks_api_key")

    while i < len(all_symbols):
        end_index = int(((i / 50) + 1) * 50)
        symbols = all_symbols[i:end_index]
        symbols = ",".join(symbols)
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
        except Exception:
            exception = sys.exc_info()
            return send_error_response(None, None, exception)
        print(response.json())
        parse_stocks_response(response.json(), i == 0)
        i += 50


def parse_stocks_response(response, record=True):
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

    if record:
        record_stocks(recorded_data)
    else:
        add_stocks(recorded_data)


def get_date():
    dt = datetime.today() - timedelta(days=1)
    return dt.strftime("%Y-%m-%d")
