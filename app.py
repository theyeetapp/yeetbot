from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from command_handlers.start import start_handler
from command_handlers.login import login_handler
from message_handlers.message import message_handler
from message_handlers.unknown import unknown_handler
import logging
import config

# Enable logging of errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# loading up all relevant variables into environment
config.set()

bot_token = config.get()['bot_token']
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    start_handler(update, context)

def login(update, context):
    login_handler(update, context)

def message(update, context):
    message_handler(update, context)

def unknown(update, context):
    unknown_handler(update, context)

start_command_handler = CommandHandler('start', start)
login_command_handler = CommandHandler('login', login)
message_command_handler = MessageHandler(Filters.text, message)
unknown_command_handler = MessageHandler(Filters.all, unknown)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(login_command_handler)
dispatcher.add_handler(message_command_handler)
dispatcher.add_handler(unknown_command_handler)

updater.start_polling()
updater.idle();