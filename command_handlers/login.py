from utilities.actions import record as record_action
import config
import os
import json

def login_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = 'Alright!, send me your Yeet email so I can begin the process of logging you in'
    context.bot.send_message(chat_id=chat_id, text=text)

    verify_path = os.path.join(config.root, 'data', 'verify.json')
    with open(verify_path, 'r') as reader:
        data = json.load(reader)

    if data[chat_id] is None:
        record_action(chat_id, 'login')