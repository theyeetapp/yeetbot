from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from command_handlers.start import start_handler
from command_handlers.login import login_handler
from command_handlers.list import list_handler
from command_handlers.list_crypto import list_crypto_handler
from command_handlers.list_stocks import list_stocks_handler
from command_handlers.update import update_handler
from message_handlers.message import message_handler
from message_handlers.unknown import unknown_handler
from middlewares.auth import authenticated, guest
from jobs.update_stocks import update_stocks
from jobs.update_crypto import update_crypto
from jobs.send_reminders import send_reminders
import logging
import config

# Enable logging of errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# loading up all relevant variables into environment
config.set()

app_config = config.get()
bot_token = app_config.get("bot_token")
bot_url = app_config.get("bot_url")
bot_host = app_config.get("bot_host")
bot_port = app_config.get("bot_port")

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
job = updater.job_queue


def start(update, context):
    start_handler(update, context)


@guest
def login(update, context):
    login_handler(update, context)


@authenticated
def list_all(update, context):
    list_handler(update, context)


@authenticated
def list_stocks(update, context):
    list_stocks_handler(update, context)


@authenticated
def list_crypto(update, context):
    list_crypto_handler(update, context)


def update(update, context):
    update_handler(update, context)


def message(update, context):
    message_handler(update, context)


def unknown(update, context):
    unknown_handler(update, context)


# job.run_once(send_reminders, 5)

start_command_handler = CommandHandler("start", start)
login_command_handler = CommandHandler("login", login)
list_command_handler = CommandHandler("list", list_all)
list_stocks_command_handler = CommandHandler("liststocks", list_stocks)
list_crypto_command_handler = CommandHandler("listcrypto", list_crypto)
update_command_handler = CommandHandler("update", update)
message_command_handler = MessageHandler(Filters.text, message)
unknown_command_handler = MessageHandler(Filters.all, unknown)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(login_command_handler)
dispatcher.add_handler(list_command_handler)
dispatcher.add_handler(list_stocks_command_handler)
dispatcher.add_handler(list_crypto_command_handler)
dispatcher.add_handler(update_command_handler)
dispatcher.add_handler(message_command_handler)
dispatcher.add_handler(unknown_command_handler)

updater.start_webhook(listen=bot_host, port=bot_port, url_path=bot_token)
updater.bot.set_webhook(url=f"{bot_url}{bot_token}")

updater.idle()
