from dotenv import load_dotenv
import os

root = os.path.dirname(__file__)


def set():
    dotenv_path = root + "/" + ".env"
    load_dotenv(dotenv_path)


def get(key: str = None):
    app_url = os.environ.get("APP_URL")
    bot_token = os.environ.get("BOT_TOKEN")
    bot_url = os.environ.get("BOT_URL")
    bot_host = os.environ.get("BOT_HOST")
    bot_port = os.environ.get("BOT_PORT")
    dome_api_key = os.environ.get("DOME_API_KEY")
    dome_api_url = os.environ.get("DOME_API_URL")
    dome_uuids = os.environ.get("DOME_UUIDS")
    stocks_api_endpoint = os.environ.get("STOCKS_API_ENDPOINT")
    stocks_api_key = os.environ.get("STOCKS_API_KEY")
    crypto_api_endpoint = os.environ.get("CRYPTO_API_ENDPOINT")
    yeet_api_url = os.environ.get("YEET_API_URL")

    config_values = {
        "bot_token": bot_token,
        "app_url": app_url,
        "bot_host": bot_host,
        "bot_port": bot_port,
        "bot_url": bot_url,
        "dome_api_key": dome_api_key,
        "dome_api_url": dome_api_url,
        "dome_uuids": dome_uuids,
        "stocks_api_endpoint": stocks_api_endpoint,
        "stocks_api_key": stocks_api_key,
        "crypto_api_endpoint": crypto_api_endpoint,
        "yeet_api_url": yeet_api_url,
    }

    return config_values if not key else config_values.get(key)
