from dotenv import load_dotenv
import mysql.connector as db_connector
import os

root = os.path.dirname(__file__)
mydb = None


def set():
    dotenv_path = root + "/" + ".env"
    load_dotenv(dotenv_path)
    db_host = os.environ.get("DB_HOST")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_DATABASE")
    global mydb
    mydb = db_connector.connect(
        host=db_host, username=db_username, password=db_password, database=db_name
    )


def get():
    bot_token = os.environ.get("BOT_TOKEN")
    app_url = os.environ.get("APP_URL")
    mail_base_url = os.environ.get("MAIL_BASE_URL")
    mail_api_key = os.environ.get("MAIL_API_KEY")
    mail_from = os.environ.get("MAIL_FROM")
    mail_from_url = os.environ.get("MAIL_FROM_URL")
    stocks_api_endpoint = os.environ.get("STOCKS_API_ENDPOINT")
    stocks_api_key = os.environ.get("STOCKS_API_KEY")
    crypto_api_endpoint = os.environ.get("CRYPTO_API_ENDPOINT")
    yeet_api_url = os.environ.get("YEET_API_URL")

    return {
        "bot_token": bot_token,
        "app_url": app_url,
        "mail_base_url": mail_base_url,
        "mail_api_key": mail_api_key,
        "mail_from": mail_from,
        "mail_from_url": mail_from_url,
        "db": mydb,
        "stocks_api_endpoint": stocks_api_endpoint,
        "stocks_api_key": stocks_api_key,
        "crypto_api_endpoint": crypto_api_endpoint,
        "yeet_api_url": yeet_api_url
    }
