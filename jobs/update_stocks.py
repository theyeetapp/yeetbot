from requests.exceptions import HTTPError
from utilities.stocks import record as record_stocks
import requests
import config
import os.path as path


def update_stocks(context):
    config_dict = config.get()
    api_endpoint = config_dict.get("stocks_api_endpoint")
    api_key = config_dict.get("stocks_api_key")
    symbols = fetch_formatted_stocks()
    print(symbols)
    date_from = "2021-08-20"
    date_to = "2021-08-20"

    try:
        response = requests.get(
            api_endpoint,
            params={
                "access_key": api_key,
                "symbols": symbols,
                "date_from": date_from,
                "date_to": date_to,
            },
        )
        response.raise_for_status()
        parse_stocks_response(response.json())
    except HTTPError as http_error:
        print(http_error)
    except Exception as error:
        print(error)


def parse_stocks_response(response):
    data = response["data"]
    recorded_data = dict()

    for content in data:
        symbol = content["symbol"]
        recorded_content = {
            "open": content["open"],
            "high": content["high"],
            "low": content["low"],
            "close": content["close"],
            "volume": content["volume"],
        }
        recorded_data[symbol] = recorded_content

    record_stocks(recorded_data)


def fetch_formatted_stocks():
    config_dict = config.get()
    db = config_dict.get("db")
    cursor = db.cursor()
    query = 'SELECT name FROM symbols WHERE type="stock"'
    cursor.execute(query)
    stocks = cursor.fetchall()
    return ",".join(list(map(get_stock_name, stocks)))


def get_stock_name(stock):
    return str(stock[0])
