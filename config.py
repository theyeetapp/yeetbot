from dotenv import load_dotenv
import os

root = os.path.dirname(__file__)

def set():
    dotenv_path = root + "/" + ".env"
    load_dotenv(dotenv_path)

def get():
    bot_token = os.environ.get("BOT_TOKEN")
    app_url = os.environ.get("APP_URL")
    stocks_api_endpoint = os.environ.get("STOCKS_API_ENDPOINT")
    stocks_api_key = os.environ.get("STOCKS_API_KEY")
    crypto_api_endpoint = os.environ.get("CRYPTO_API_ENDPOINT")
    yeet_api_url = os.environ.get("YEET_API_URL")

    return {
        "bot_token": bot_token,
        "app_url": app_url,
        "stocks_api_endpoint": stocks_api_endpoint,
        "stocks_api_key": stocks_api_key,
        "crypto_api_endpoint": crypto_api_endpoint,
        "yeet_api_url": yeet_api_url,
    }
