from dotenv import load_dotenv
import os

root = os.path.dirname(__file__)

def set():
    dotenv_path = root + '/' + '.env'
    load_dotenv(dotenv_path)

def get():
    bot_token = os.environ.get('BOT_TOKEN')
    app_url = os.environ.get('APP_URL')

    return {"bot_token":bot_token, "app_url":app_url};



