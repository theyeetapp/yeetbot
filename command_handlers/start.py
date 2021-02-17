from telegram import ParseMode
from utilities.actions import record as record_action
import os
import json
import random
import config

def start_handler(update, context):
    greetings = ['Hey', 'Hola', 'Hey there', 'Heyaa', 'Hi', 'Hello']
    chat_id = str(update.effective_chat.id)
    greeting = greetings[random.randint(0, len(greetings) - 1)]
    app_url = config.get()['app_url']

    with open(os.path.join(config.root, 'messages', 'start.txt'), 'r') as reader:
        start_message = greeting + reader.read().format(app_url, app_url, app_url + 'signup')

    context.bot.send_message(chat_id=chat_id, text=start_message, parse_mode=ParseMode.HTML)

    verify_path = os.path.join(config.root, 'data', 'verify.json')
    with open(verify_path, 'r') as reader:
        data = json.load(reader)

    if data[chat_id] is None:
        record_action(chat_id, 'start')