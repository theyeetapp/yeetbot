from telegram import ParseMode
from utilities.actions import record as record_action
import utilities.verify as verify
import os
import random
import config


def start_handler(update, context):
    greetings = ["Hey", "Hola", "Hey there", "Heyaa", "Hi", "Hello"]
    chat_id = str(update.effective_chat.id)
    greeting = greetings[random.randint(0, len(greetings) - 1)]
    app_url = config.get()["app_url"]

    with open(os.path.join(config.root, "messages", "start.txt"), "r") as reader:
        text = greeting + reader.read().format(app_url, app_url, app_url + "signup")

    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

    verify_data = verify.get()
    if verify_data.get(chat_id) is None:
        record_action(chat_id, "start")
