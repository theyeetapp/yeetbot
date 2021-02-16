from dotenv import load_dotenv
import mysql.connector as db_connector
import os

root = os.path.dirname(__file__)
mydb = None

def set():
    dotenv_path = root + '/' + '.env'
    load_dotenv(dotenv_path)
    db_host = os.environ.get('DB_HOST')
    db_username = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_DATABASE')
    global mydb
    mydb = db_connector.connect(host=db_host, username=db_username, password=db_password, database=db_name)

def get():
    bot_token = os.environ.get('BOT_TOKEN')
    app_url = os.environ.get('APP_URL')

    return {"bot_token":bot_token, "app_url":app_url, "db":mydb};



