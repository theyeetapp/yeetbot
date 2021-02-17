from config import root
from message_handlers.login_mail import login_mail
from message_handlers.login_complete import login_complete
from message_handlers.unknown import unknown_handler
import os.path as path
import json

def message_handler(update, context):
    chat_id = str(update.effective_chat.id)
    actions_path = path.join(root, 'data', 'actions.json')
    with open(actions_path, 'r') as reader:
        actions = json.load(reader)
    
    action = actions[chat_id]

    if action is None:
        return context.bot.send_message(chat_id=chat_id, text='I am sorry. I do not understand that')

    if action == 'login':
        return login_mail(update, context)

    if action == 'login_email':
        return login_complete(update, context)

    return unknown_handler(update, context)